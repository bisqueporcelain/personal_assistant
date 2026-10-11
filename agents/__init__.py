"""Agent definitions for the semester assistant.

The orchestrator runs as the main session and delegates to the two workers via
the `Agent` tool. Each worker owns one kind of deliverable and carries the skill
that supplies its method:

    orchestrator  routing, course-fact lookup, integrity gate   (main session)
      ├─ writer     prose deliverables                          `writing` skill
      └─ scheduler  deadlines, sequencing, action plans         no skill

Agent *definitions* carry method and posture. Course *facts* live in `courses/`
and are read at runtime — the same split the skills enforce. Nothing here is
specific to one person's semester.
"""

from .orchestrator import ORCHESTRATOR, ORCHESTRATOR_SYSTEM_PROMPT
from .scheduler import SCHEDULER
from .writer import WRITER

#: Subagents the orchestrator may delegate to. This is what goes into
#: `ClaudeAgentOptions.agents` — the orchestrator itself is the main session,
#: so it is deliberately absent.
SUBAGENTS = {
    "writer": WRITER,
    "scheduler": SCHEDULER,
}

#: Every agent including the orchestrator, for the cases where the orchestrator
#: is delegated to rather than run directly (nested or background sessions).
ALL_AGENTS = {
    "orchestrator": ORCHESTRATOR,
    **SUBAGENTS,
}

__all__ = [
    "ALL_AGENTS",
    "ORCHESTRATOR",
    "ORCHESTRATOR_SYSTEM_PROMPT",
    "SCHEDULER",
    "SUBAGENTS",
    "WRITER",
]
