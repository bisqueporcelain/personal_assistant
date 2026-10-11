# Semester assistant

A personal course assistant built on the
[Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview). It reads
your syllabi, routes each request to the agent that owns that kind of work, and
calibrates writing feedback against prose you wrote yourself.

It is designed so that **the method is shareable and the data never leaves your
machine.** Agent definitions and skills carry technique; your courses, syllabi,
notes, writing samples, and conversation history are gitignored or live in a
local database.

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

agents/
  orchestrator.py           routing, course-fact lookup, integrity gate
  writer.py                 prose deliverables — critique, not ghostwriting
  scheduler.py              deadlines and sequencing — read-only, quotes dates
email_writer.py             correspondence helper

db/
  schema.sql                conversations, turns, metrics, continuity notes
  store.py                  asyncpg store, plus a no-op fallback

.claude/skills/
  writing/SKILL.md          method: analysis, critique, composition, documentation
  technical/SKILL.md        method: algorithms, contests, hardware, debugging
  */local.md                your private additions — gitignored, read if present

courses/
  EXAMPLE.md                the schema, tracked
  *.md                      your courses — instructors, weights, rubrics, dates

syllabi/                    raw syllabus text
ongoing_processes/          situations in flight — extensions, advising threads
writing_samples/            your prose, for calibrating critique
  voice-profile.md          derived from your samples
```

The division of labor is the whole design:

| | Contains | Tracked |
|---|---|---|
| **Agents** | Who handles what, and with what posture. | Yes |
| **Skills** | How to help. "Ask for the approach before giving a solution." | Yes |
| **Schema** | The shape of the conversation log. | Yes |
| **Course files** | What is true about one semester. Due dates, weights, rubrics. | No |
| **Samples** | How you write. | No |
| **Conversation history** | What was said. Lives in PostgreSQL. | No |

An agent that needs a fact it does not have is instructed to **say so and
stop**, not to guess. A guessed due date is worse than an admitted gap.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Then:

1. Drop your syllabi into `syllabi/`.
2. Copy `courses/EXAMPLE.md` to `courses/<your-course>.md` and fill it in, one
   file per course. This is the step that teaches the agent your semester.
3. Add a few pieces of your own writing to `writing_samples/` — see that
   folder's README.
4. Set up the database below, or skip it and run without history.
5. `python agent.py`

### Database setup

Conversation history lives in PostgreSQL so a session can pick up where the last
one stopped. On macOS with Homebrew:

```bash
brew install postgresql@17
brew services start postgresql@17
createdb fall_semester_assistant
```

The schema is created automatically on first run. To point at a different
server, copy `.env.example` to `.env` and set `SEMESTER_DB_DSN`.

**The database is optional.** With no server reachable, `agent.py` prints a
warning and runs anyway — you lose continuity between runs, nothing else.

### Running it

```bash
python agent.py                       # interactive, resumes the default thread
python agent.py --thread cinema       # a separate thread with its own history
python agent.py --fresh               # ignore stored history, start over
python agent.py "what is due friday"  # one question, then exit
python agent.py --require-db          # fail rather than run without history
```

## Conversational consistency

Two mechanisms, because they fail differently.

**Session resumption** is the good path. Every completed turn writes the Claude
Agent SDK's `session_id` to `conversations.sdk_session_id`; the next run passes
it back as `resume`, and the model picks up its own transcript with full
context. The id is rewritten on every turn rather than just the first, because
compaction and forking can both hand back a different one, and resuming a stale
id silently loses everything after the fork.

**The turn log** is the fallback. When a transcript cannot be resumed — pruned
off disk, a different machine, a crash mid-turn — the SDK would otherwise start
blank. `continuity_primer()` rebuilds a short briefing from the last few turns
and any standing notes, and `agent.py` appends it to the system prompt so the
new session opens knowing what the last one concluded. It is built only when
resumption fails; when `resume` works, a reconstruction would just compete with
the real history.

The split matters: the SDK transcript is authoritative for *what was said*, and
the database for *what must be remembered*. Neither stores a course fact. Those
stay in `courses/`, where going stale is visible.

## Roadmap

Ordered roughly by how much each unblocks the others.

### Core

- [ ] **Flesh out the `writing` skill.** The current file establishes method and
      the sample-ingestion protocol. Still owed: worked examples of critique at
      each level (thesis, structure, paragraph, line), a genre-by-genre account
      of what "good" means for analysis vs. reflection vs. language
      composition, explicit handling of the revise-after-feedback loop, and
      calibration guidance for how hard to push on a draft that is nearly due
      versus one in its first pass. **This is the primary deliverable.**
- [ ] **Syllabus ingestion.** A script that reads `syllabi/` and writes
      `courses/<name>.md` in the `EXAMPLE.md` schema, so onboarding is one
      command instead of an hour of transcription. Currently the hard edge for
      anyone who is not the author.
- [ ] **Voice-profile generation.** Implement the derivation the `writing` skill
      describes: read samples per genre, extract the named dimensions, write
      `writing_samples/voice-profile.md` with quoted evidence, regenerate when
      samples change.
- [ ] **Finish `email_writer.py`.** The file is a stub. The `writing` skill
      already routes correspondence to it.
- [ ] **A `builder` agent for technical coursework.** The `technical` skill has
      no agent of its own, so the orchestrator currently invokes it in-session.
      That reintroduces exactly the problem the skill split was meant to solve —
      prose help should withhold text, technical help should withhold solutions,
      and one prompt holding both collapses toward whichever came last. The
      fourth agent is the fix.

### Quality

- [x] Integrity check as a real gate, not a reminder: the orchestrator reads the
      course's AI clause before delegating, and the check is not delegated.
- [x] Deadline awareness — the `scheduler` agent reads dates from `courses/*.md`
      and orders work by weight against remaining time.
- [ ] Have the agents write their own `continuity_notes` rows, rather than only
      `agent.py` logging turns. A decision reached mid-session is the thing most
      worth carrying forward and the thing a turn log preserves worst.
- [ ] Prune the turn log. Nothing deletes old rows, and the primer reads only
      the newest few, so the table grows without bound for no benefit.
- [ ] Per-genre critique examples in `writing_samples/` as tracked fixtures
      (synthetic prose, not anyone's real work) so the skill has worked
      examples that ship with the repo.

### Open source

- [ ] Verify a cold clone works: no `courses/`, no samples, no syllabi. The
      agent should explain what it needs rather than fail or hallucinate.
- [ ] Prompt the skills' descriptions and routing against a second user's
      course load to find Columbia-shaped assumptions that survived extraction.
- [ ] Contributing guide — what belongs in a skill (method) versus a course file
      (facts), so contributions do not re-mix the two.
- [ ] License.

## Design notes

**Why skills instead of one long system prompt.** Course help splits cleanly
into prose work and build work, and the two want opposite defaults: writing help
should withhold text and critique instead, technical help should withhold
solutions and ask for an approach. One prompt holding both tends to collapse
toward whichever instruction came last.

**Why course facts are data.** They go stale every semester, they differ per
student, and they are the only part a model is tempted to invent. Keeping them
in files makes the staleness visible and the invention impossible.

**Why samples never generate prose.** Every syllabus here that addresses AI
requires that submitted work be explainable by the student. Text generated in
your own voice is exactly the thing you cannot explain. The limit is in the
skill, the samples README, and the integrity sections — deliberately
redundant.

**Why separate agents instead of one orchestrator with three modes.** Same
argument as the skill split, one level up. The writer's default is to withhold
prose and critique instead; the scheduler's is to refuse any date it cannot
quote. Those are different refusals, and a single prompt carrying both tends to
apply whichever was stated most recently. Separate agents also mean separate
tool surfaces — the scheduler has no `Write`, so it cannot edit a draft even if
asked, and the writer has no `Agent`, so it cannot re-delegate its own job.

**Why the database stores conversation and not course facts.** They go stale on
opposite schedules. A due date changes when an instructor changes it, and the
only safe way to notice is to read the file where it is written. What was said
last Tuesday does not change at all, which is exactly what makes it worth
caching. Mixing the two would put a quotable fact behind a layer that looks
authoritative and is not.

**Why craft guidance is paraphrased, not quoted at length.** The `writing`
skill's section on building a first-person narrator summarizes Phillip Lopate
rather than reproducing him. A public repository that carries a chapter of
someone else's book is redistributing it, and the annotations — what the move
is and why it works — are the part that makes the skill useful anyway.
