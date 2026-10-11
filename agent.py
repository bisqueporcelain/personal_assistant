"""Entry point for the semester assistant.

Runs the orchestrator as an interactive session, with the writer and scheduler
available to it as subagents, and persists the conversation to PostgreSQL so the
next run picks up where this one stopped.

    python agent.py                       # the default thread
    python agent.py --thread cinema       # a separate thread, own history
    python agent.py --fresh               # ignore stored history, start over
    python agent.py "what is due friday"  # one question, then exit

Nothing here is specific to one person's semester. The facts come from
`courses/`, the method from `.claude/skills/`, and the history from the database.
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import datetime as dt
import sys
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ThinkingBlock,
    ToolUseBlock,
)

from agents import ORCHESTRATOR_SYSTEM_PROMPT, SUBAGENTS
from db import Thread, open_store

PROJECT_ROOT = Path(__file__).resolve().parent

MODEL = "claude-opus-5"

#: Directories the session may read beyond the project root. Each is gitignored;
#: the agent reads them, the repository never carries them.
DATA_DIRS = ("courses", "syllabi", "ongoing_processes", "writing_samples")

#: Read-only tools the orchestrator uses constantly. Pre-allowing them keeps the
#: session from prompting on every course-file lookup. The writer's `Write` and
#: `Edit` are deliberately absent, so touching a draft still asks first.
AUTO_ALLOWED = ("Read", "Grep", "Glob", "Agent", "Skill")


def build_system_prompt(primer: str, today: dt.date) -> str:
    """The orchestrator prompt, plus today's date and any carried-over context.

    The date has to be injected rather than recalled: the scheduler refuses to
    infer one, and a model's idea of "today" is whenever it was trained.
    """
    parts = [
        ORCHESTRATOR_SYSTEM_PROMPT,
        f"## Today\n\nToday's date is {today.isoformat()} ({today:%A}). Use this "
        f"date for every calculation about what is due or how much time remains, "
        f"and pass it to the scheduler when you delegate.",
    ]
    if primer:
        parts.append(primer)
    return "\n\n".join(parts)


async def run_turn(client: ClaudeSDKClient, store, thread: Thread, prompt: str) -> None:
    """Send one prompt, stream the reply, and persist both sides."""
    await store.append_turn(thread, "user", prompt)

    reply: list[str] = []
    model_used: str | None = None

    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            model_used = message.model
            for block in message.content:
                if isinstance(block, TextBlock):
                    reply.append(block.text)
                    print(block.text, end="", flush=True)
                elif isinstance(block, ThinkingBlock):
                    continue
                elif isinstance(block, ToolUseBlock):
                    # Surface delegation, since a subagent's own output is not
                    # streamed back here — only its final report to the
                    # orchestrator is.
                    if block.name == "Agent":
                        worker = block.input.get("subagent_type", "?")
                        print(f"\n  → delegating to {worker}…", flush=True)

        elif isinstance(message, ResultMessage):
            print()
            turn_id = await store.append_turn(
                thread,
                "assistant",
                "".join(reply),
                agent="orchestrator",
                model=model_used,
            )
            await store.record_metrics(
                turn_id,
                num_turns=message.num_turns,
                duration_ms=message.duration_ms,
                cost_usd=message.total_cost_usd,
                stop_reason=message.stop_reason,
                is_error=message.is_error,
                usage=message.usage,
            )
            # Written every turn: compaction or a fork can hand back a
            # different session id than the one we resumed from.
            await store.record_session(thread, message.session_id)

            if message.is_error:
                print(f"[error] {message.subtype}: {message.result}", file=sys.stderr)
            if message.total_cost_usd:
                print(f"  ({message.num_turns} turns, ${message.total_cost_usd:.4f})")


async def repl(client: ClaudeSDKClient, store, thread: Thread) -> None:
    """Read prompts until EOF or an exit command."""
    print("Ask a question, or Ctrl-D to exit.\n")
    loop = asyncio.get_running_loop()

    while True:
        try:
            # input() blocks the event loop; hand it to a thread so streaming
            # and any background subagent keep running.
            prompt = await loop.run_in_executor(None, input, "you> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return

        prompt = prompt.strip()
        if not prompt:
            continue
        if prompt in {"exit", "quit", r"\q"}:
            return

        await run_turn(client, store, thread, prompt)
        print()


async def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "prompt",
        nargs="*",
        help="Ask one question and exit. Omit for an interactive session.",
    )
    parser.add_argument(
        "--thread",
        default="default",
        help="Conversation to continue. Separate threads keep separate history.",
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Start a new conversation instead of resuming the stored one.",
    )
    parser.add_argument(
        "--require-db",
        action="store_true",
        help="Fail if PostgreSQL is unreachable, instead of running without history.",
    )
    args = parser.parse_args(argv)

    store = await open_store(required=args.require_db)
    try:
        thread = await store.open_thread(args.thread)

        resume_from = None if args.fresh else thread.sdk_session_id
        # The primer only earns its tokens when the SDK cannot resume its own
        # transcript. When `resume` works, the model already has the real
        # history and a reconstruction would just compete with it.
        primer = "" if resume_from else await store.continuity_primer(thread)

        if resume_from:
            print(f"[{args.thread}] resuming session {resume_from}")
        elif primer:
            print(f"[{args.thread}] new session, carrying over earlier context")
        else:
            print(f"[{args.thread}] new conversation")

        options = ClaudeAgentOptions(
            system_prompt=build_system_prompt(primer, dt.date.today()),
            model=MODEL,
            cwd=PROJECT_ROOT,
            add_dirs=[PROJECT_ROOT / name for name in DATA_DIRS],
            agents=SUBAGENTS,
            # The orchestrator handles technical coursework itself for now; see
            # README "Roadmap" — a builder agent is the right home for it.
            skills=["writing", "technical"],
            allowed_tools=list(AUTO_ALLOWED),
            resume=resume_from,
            fork_session=False,
        )

        async with ClaudeSDKClient(options) as client:
            if args.prompt:
                await run_turn(client, store, thread, " ".join(args.prompt))
            else:
                await repl(client, store, thread)
    finally:
        await store.close()

    return 0


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        raise SystemExit(asyncio.run(main()))
