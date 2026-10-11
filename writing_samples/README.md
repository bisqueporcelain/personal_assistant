# Writing samples

Put your own prose here. The `writing` skill reads it to calibrate critique, so
that feedback measures a draft against *your* best work instead of against a
generic standard. Nothing in this folder is committed — only this README and
`.gitkeep` are tracked, so your coursework stays on your machine.

## Why bother

Generic writing feedback converges on the same advice for everyone: tighten the
thesis, vary the sentence length, add a transition. It is not wrong, and it is
not useful. Feedback that can say *"your Varda paragraph put the claim in the
first sentence and this draft buries it in the fourth"* is useful, because it
names a standard you have already met.

## How to organize it

Group by genre in subfolders. Voice is genre-dependent — the same person writes
a film analysis and a lab reflection differently, and a profile averaged across
both describes nobody.

```
writing_samples/
  analysis/        film and text analysis, close reading
  essays/          argumentative and research essays
  reflections/     blog posts, learning logs, design write-ups
  language/        foreign-language composition
  correspondence/  emails to instructors, petitions, requests
  voice-profile.md derived automatically — do not hand-edit
```

Use whatever subfolders match your coursework; the names above are a starting
point, not a fixed schema.

## What makes a good sample

In rough order of value:

1. **Graded work with instructor comments.** The most valuable artifact you can
   add. It shows not just how you write but what a grader in that discipline
   rewards, and the skill is instructed to defer to the instructor's priorities
   over its own preferences.
2. **Work you were happy with.** The target the critique aims at.
3. **Work you were unhappy with,** labeled as such. Useful for identifying tics
   — but say so, or it gets read as a target.
4. **Drafts alongside their revisions.** These show what your revision process
   already catches, so feedback can skip it.

Three to five pieces per genre is plenty. Thirty is not better.

## Label your samples

Add a short header to each file, or a `notes.md` in the subfolder. Without
provenance, an unmarked first draft and a returned A paper look identical:

```
Course: FREN UN3587
Assignment: Critical Film Review
Grade: A-
Revised: yes, after TA feedback
Notes: instructor flagged the conclusion as summary rather than argument
```

## The voice profile

The skill derives `voice-profile.md` from your samples: per-genre observations
with quoted evidence, a list of recurring tics to flag in future drafts, and a
list of strengths to preserve. It regenerates when you add or change samples.

Read it. It is the most direct statement of your habits you are likely to get,
and you can disagree with it — tell the agent where it is wrong and that goes
into the profile too.

## What this is not for

**Samples calibrate feedback. They never generate submitted prose.** The skill
will not use your voice profile to write text you hand in, and it will refuse
to produce imitations of your writing — the closer the imitation, the clearer
the violation. What it offers instead is an outline, a critique of what you
wrote, a counter-argument to answer, or a list of what the draft has not
addressed yet.

That limit is the point of the design, not a concession in it. Every course
syllabus in `courses/` that mentions AI requires that you be able to explain
what you submit; prose generated in your own voice is precisely the thing you
cannot explain.
