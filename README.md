# Semester assistant

A personal course assistant built on the
[Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview). It reads
your syllabi, routes each request to the agent that owns that kind of work, and
calibrates writing feedback against prose you wrote yourself.

The method is shareable; the data never leaves your machine. Agents and skills
carry technique. Your courses, syllabi, notes, samples, and history are
gitignored or live in a local database.

## How it works

An orchestrator holds the semester's facts and delegates to two workers:

```
                      ┌──────────────┐
      you ───────────▶│ orchestrator │  routes, quotes course facts,
                      └──────┬───────┘  gates on the integrity clause
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
        ┌──────────┐                 ┌───────────┐
        │  writer  │                 │ scheduler │
        └──────────┘                 └───────────┘
      prose deliverables          what is due, in what
      `writing` skill             order, what slipping costs
```

```
agent.py                    entry point — session, REPL, persistence wiring
email_writer.py             correspondence helper

agents/                     orchestrator, writer, scheduler
db/                         schema.sql, store.py (asyncpg, with no-op fallback)
.claude/skills/             writing/ and technical/ method files
courses/                    one file per course — EXAMPLE.md is the schema
syllabi/                    raw syllabus text
ongoing_processes/          situations in flight — extensions, advising threads
writing_samples/            your prose, for calibrating critique
```

Tracked: agents, skills, schema. Untracked: course files, samples, conversation
history. An agent that needs a fact it does not have says so and stops rather
than guessing — a guessed due date is worse than an admitted gap.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Then:

1. Drop your syllabi into `syllabi/`.
2. Copy `courses/EXAMPLE.md` to `courses/<your-course>.md`, one file per course.
   This is the step that teaches the agent your semester.
3. Add a few pieces of your own writing to `writing_samples/` — see that
   folder's README.
4. Set up the database below, or skip it and run without history.
5. `python agent.py`

### Database

Conversation history lives in PostgreSQL so a session can pick up where the
last one stopped. On macOS with Homebrew:

```bash
brew install postgresql@17
brew services start postgresql@17
createdb fall_semester_assistant
```

The schema is created on first run. To point at a different server, copy
`.env.example` to `.env` and set `SEMESTER_DB_DSN`. The database is optional:
with no server reachable, `agent.py` warns and runs anyway — you lose
continuity between runs, nothing else.

### Running it

```bash
python agent.py                       # interactive, resumes the default thread
python agent.py --thread cinema       # a separate thread with its own history
python agent.py --fresh               # ignore stored history, start over
python agent.py "what is due friday"  # one question, then exit
python agent.py --require-db          # fail rather than run without history
```

## Design notes

**Continuity has two mechanisms.** Each turn stores the SDK's `session_id`, and
the next run passes it back as `resume` so the model picks up its own
transcript. When that fails — pruned, different machine, crash mid-turn —
`continuity_primer()` rebuilds a short briefing from the last few turns and any
standing notes. The transcript is authoritative for *what was said*, the
database for *what must be remembered*. Neither stores a course fact.

**Why skills and separate agents, not one long prompt.** Writing help should
withhold text and critique instead; technical help should withhold solutions
and ask for an approach; the scheduler should refuse any date it cannot quote.
Those are different refusals, and one prompt carrying all of them collapses
toward whichever was stated last. Separate agents also mean separate tool
surfaces — the scheduler has no `Write`, the writer has no `Agent`.

**Why course facts are data.** They go stale every semester, differ per student,
and are the only part a model is tempted to invent. Files make the staleness
visible and the invention impossible.

**Why samples never generate prose.** Submitted work has to be explainable by
the student, and text generated in your own voice is exactly what you cannot
explain. The limit is stated in the skill, the samples README, and the
integrity sections — deliberately redundant.

**Why craft guidance is paraphrased.** A public repository carrying a chapter of
someone else's book is redistributing it, and the annotations — what the move is
and why it works — are the useful part anyway.
