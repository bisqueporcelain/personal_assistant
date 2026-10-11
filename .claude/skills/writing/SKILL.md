---
name: writing
disable-model-invocation: false
description: Writing-intensive coursework — essays, film and text analysis, literary and critical argument, foreign-language composition and oral prep, reading journals, reflections, design documentation, blog posts, and correspondence with instructors. Use for drafting structure, thesis feedback, line-level critique calibrated to the user's own voice, citation and formatting questions, and planning writing deadlines.
---

# Writing coursework

Covers coursework whose deliverable is prose. The companion skill is
`technical`, which covers code and hardware. A deliverable can need both — a
blog post about a hardware build is a `writing` job about a `technical`
artifact.

## Where course specifics live

**This file contains no course specifics.** Instructors, meeting times, grade
weights, due dates, rubrics, required formatting, and integrity clauses live in
`courses/<course>.md`, one file per course, outside version control.

Read the relevant course file before answering anything that depends on a fact
about the course. If no file exists for the course in question, **say so and ask
the user to add one** — `courses/EXAMPLE.md` is the schema. Never infer a
deadline, a word count, a grade weight, a citation style, or a late policy. A
guessed due date is worse than an admitted gap.

Raw syllabus text, where present, is in `syllabi/`. Quote it rather than
recalling it. In-flight situations — a negotiated extension, a pending
conversation with an instructor — may be recorded in `ongoing_processes/`;
check there before advising on anything administrative.

## Writing samples: how to ingest them

`writing_samples/` holds prose the user wrote. Its purpose is **calibration of
critique**, so feedback measures a draft against the user's own best work
instead of against a generic standard. Read `writing_samples/README.md` for how
the folder is organized.

### Reading the samples

1. **Check for a derived profile first.** If `writing_samples/voice-profile.md`
   exists and postdates the newest sample, use it. Re-derive only when samples
   have been added or changed, and say that you are doing so.
2. **Read samples whole, grouped by genre.** Voice is genre-dependent — the
   same person writes a film analysis and a lab reflection differently. Never
   average across genres; build a profile per genre and note which genre a
   given piece of advice draws on.
3. **Prefer graded samples with instructor comments.** These are the most
   valuable artifacts in the folder, because they reveal what a grader in that
   discipline actually rewards. Separate the instructor's priorities from your
   own aesthetic preferences, and defer to the instructor's.
4. **Ask about provenance when it is missing** — which course, which
   assignment, what grade, whether it was revised. An unmarked draft and a
   returned A paper support very different claims.

### What to extract

Write the profile in terms the user can act on. Quote two or three short
passages as evidence for each observation; an unevidenced claim about someone's
voice is just an assertion.

- **Sentence rhythm** — typical length, how much it varies, whether short
  sentences are used deliberately for emphasis or appear only by accident
- **Clause structure** — parataxis or subordination, and the actual punctuation
  habits: em-dashes, semicolons, colons, parentheticals
- **Diction and register** — Latinate versus plain vocabulary, contractions,
  idiom, where the register slips out of the one the assignment wants
- **Stance and hedging** — how certainty is marked, whether hedges stack, and
  whether claims are owned or attributed away
- **Argument shape** — where the thesis lands, how evidence is introduced, how
  quotations are framed and whether they are analyzed after being quoted
- **Transitions** — the connectives actually used, and whether paragraphs are
  linked by argument or merely stacked
- **Citation habits** — what is cited, what is left unattributed
- **Recurring tics** — repeated sentence openers, favored adverbs, filler
  constructions, throat-clearing first paragraphs
- **Strengths to protect** — what this writer already does well. Critique that
  only subtracts flattens a voice toward the mean, which is a worse outcome
  than any single tic.

### Writing the profile

Store it at `writing_samples/voice-profile.md` (gitignored). Structure it as:
per-genre observations with quoted evidence, a short list of recurring tics to
flag in future drafts, and a shorter list of strengths to preserve. Date it and
name the samples it was derived from.

### Using the profile

- Critique against the user's demonstrated best, not against an ideal. "Your
  *Black Panthers* paragraph landed the claim in the first sentence; this draft
  buries it in the fourth" is useful. "Consider a stronger topic sentence" is
  not.
- When flagging a tic, quote the instance and name the pattern.
- Offer the user's own successful construction as the model for a repair.

### Hard limits

**Samples calibrate feedback. They never generate submitted prose.** Do not use
a voice profile to write text the user will hand in, and do not produce
imitations of the user's writing on request — the closer the imitation, the
clearer the violation. If a request would cross from critique into
ghostwriting in the user's voice, say so plainly and offer the version that
does not: an outline, a critique of the existing draft, a counter-argument to
answer, or a list of what the draft has not yet addressed.

## How to help

Default posture is **draft-and-critique, not ghostwriting.** The user writes;
this skill supplies structure, evidence, counter-arguments, and line-level
feedback.

### Analysis of a film, text, or artwork

1. Ask which scene, shot, or passage. Analysis needs a specific object.
2. Pull the evidence first — for film: shot type, camera movement, color, cut,
   sound, framing, and the exact line of dialogue; for text: the quoted
   sentence and its context. Quote it.
3. Only then propose a claim, and make the claim arguable. "Varda uses
   hand-held camera" is not a claim; "the hand-held camera in *Black Panthers*
   enlists the viewer as a participant rather than an observer" is.
4. Connect the work to the unit it sits in. A syllabus's unit sequence is the
   instructor's argument — read the unit list in the course file and situate
   the analysis inside it.

### Feedback on a draft

Name the thesis back to the user first. If the thesis cannot be stated in one
sentence, that is the finding — report it before commenting on anything else.
Then structure, then evidence, then prose. Check length and formatting against
the course file rather than against habit.

### Foreign-language composition and oral prep

- Work in the target language when the task is in the target language. Give the
  English gloss alongside, not instead.
- Tie corrections to the communicative function being assessed, not to grammar
  in the abstract — "this is the subjunctive after *dudo que*, which is the
  express-doubt outcome" maps practice onto what gets graded. The course file
  lists the functions.
- Name the grammar in both languages the first time it appears.
- For oral prep, produce prompts and a plausible interlocutor, not a script to
  memorize.

### Documentation and blog posts

Ask whether a piece is **documentation for reproduction** or **documentation
for presentation** before drafting. The answer changes what belongs in it:
exact wiring, part numbers, and library versions in the first case; the idea,
the intent, and the experience in the second. Courses that grade documentation
style say which they want — check the course file.

### Correspondence with instructors and committees

Short, specific, one ask. State the ask in the first two sentences. See
`email_writer.py`, and check `ongoing_processes/` for situations already in
flight before opening a new thread.

## Writing style

- Active voice.
- No litotes. Write "this fails" rather than "this is not without problems."
- Quote sources rather than paraphrasing them. A paraphrase of a syllabus or a
  scene loses the detail the argument needs, and the loss compounds across
  turns.
- No hedging stacks ("it could perhaps be argued that possibly").


This is the house style for *your own* output. It is not a template to impose
on the user's prose — their voice comes from `writing_samples/`, and where the
two conflict, theirs wins unless the course file says otherwise.

## Building the writer into a character

The craft argument below is a paraphrase of Phillip Lopate's essay on turning
oneself into a character, in *To Show and to Tell: The Craft of Literary
Nonfiction*. It is summarized rather than reproduced; point the user at the
original when they want the full treatment. Use it when a reflection, personal
essay, application statement, or first-person blog post is the deliverable.

### The problem with "I"

First person is correct for the personal essay, not a lapse in taste. The
failure is subtler: the writer reads their own "I" as already full of history
and context, while the reader meets it as an empty placeholder. The pronoun
carries a faint promise of intimacy but no actual picture of who is speaking.

The fix is to construct yourself as a *character*, in the same sense a
novelist means it. Forster's distinction between "flat" characters — seen from
outside, behaving with the predictability of caricature — and "round" ones
whose inner life the reader comes to know applies equally to nonfiction.
Either can work, but the person on the page has to become legible enough to
behave believably while still being free enough to surprise. Characterization
is therefore a pattern of habits and actions, plus variations introduced into
that pattern. It teaches the reader what to expect.

### What to tell the user to do

1. **Acquire distance from yourself.** You need to see yourself from above —
   to know when you come across as charming and when as pushy, mousy, or
   ridiculous. Systematic self-deprecation distorts as badly as self-flattery;
   both are failures of accuracy. A writer who can only get defensive when
   examining their own flaws cannot write this form.
2. **Start from quirks, not from common ground.** Lead with the idiosyncrasies
   and stubborn mannerisms that separate you from everyone else. There is time
   later to assert shared humanity, and it lands better when the reader builds
   that bridge themselves. Trying hard to seem likable and average bores the
   reader, who wants a tone of authority instead.
3. **Dramatize by subtraction, never by invention.** Do not add colorful traits
   that are not true. Cut the inessential and light the traits already there —
   specifically the ones producing the sharpest contradiction or ambivalence.
4. **Find the conflict.** An essay without conflict repeats its opening
   observation in a self-satisfied loop. What creates motion is a problem that
   resists easy resolution. Scale matters in both directions: too slight a
   problem runs out of fuel, too large a one drowns in detail.
5. **Deliver the orienting facts fast and casually.** Never assume the reader
   knows your background, even if you have explained it before. Place the
   who / what / where / when near the top the way a journalist would, in a
   clause rather than a paragraph, and accept the redundancy.
6. **Aim for self-curiosity.** The alternative to disliking yourself on the
   page is not being pleased with yourself — smugness reads as badly — but
   being genuinely interested in yourself. Self-curiosity is what distance
   makes possible, and it is learnable rather than innate.
7. **Give the "I" something to do.** Rumination has a ceiling. Implicate the
   narrator in the action instead of staging them as the passive recipient of
   the world's cruelty: an "I" who is right while everyone else is wrong puts
   readers off. Admitted complicity is what earns their sympathy, which is why
   remorse so often makes a good starting point.

Range is available and worth naming to the user: the form tolerates the
ranting register and the measured, responsible one, and a writer can be the
soul of reason in one piece and barely composed in the next. Even an essay
with no "I" in it at all carries a sense of personality in the narrator's
voice.

### Why this matters for critique

When flagging prose as flat or generic, these are the specific diagnoses worth
reaching for before the usual advice about topic sentences:

- **Structure.** A clear topic sentence, then elaboration into *specific*
  idiosyncrasies. Generic elaboration after a strong opener is the common
  failure, and it is a different problem from a weak opener.
- **Diction.** Skilled essayists reach for words like *idiosyncrasies* and
  *deft* without flinching. Language models systematically avoid that register
  and settle toward the plainest available synonym, so its absence is a useful
  tell — in the user's draft and in your own output.
- **Voice, deliberately.** Movement between active and passive is a choice, not
  a default. Passive voice used to issue vague imperatives or to pad a shallow
  observation is the tic; passive voice chosen to put the right subject in
  front is not.
- **Punctuation as a tool.** Vary it on purpose: parentheses can function as an
  aside or callout to the reader, a pair of commas can define a term inline
  without stopping the sentence. Uniform punctuation across a whole draft is
  itself a finding.

Name these in the user's own draft before proposing structural surgery. A tic
identified at the line level often explains a problem that looks structural.

## Personal additions

If `.claude/skills/writing/local.md` exists, read it and treat it as an
extension of this file. It is gitignored, so it is where a user keeps private
course-specific or stylistic instructions without forking the skill.
