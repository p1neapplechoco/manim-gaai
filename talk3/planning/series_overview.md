# V5 Series Overview

## Purpose

V5 is a concept-complete academic video series that covers the full 77-slide LfO tutorial without converting slides one-by-one. The series explains why Learning-from-Observation is a task interface: it extracts reusable task intent from observation, represents that intent as state transitions, and delegates embodiment-specific control to feedback-driven skill agents.

## Audience Type

Academic robotics audience.

## Tier

Tier 3 full tutorial series. Each chapter can be implemented as an independent ManimCE video. Runtime is coverage-first and may be below 4-6 minutes when the chapter still covers the required concepts with clear narration, subtitles, and visual explanation.

## Central Thesis

LfO generalizes because task intent is represented as domain-specific state transitions containing `what-to-do` and `where-to-do`, while reusable skill agents determine `how-to-do` through local feedback on each robot body.

## Chapter List

| Chapter | Title | Source slides | Role in series | Handoff object |
|---|---|---:|---|---|
| 01 | LfO Problem And Architecture | 1-17 | Establish motivation, encoder, task model, and skill-library architecture. | Task model card |
| 02 | Contact-State Representation And Primitive Actions | 18-26 | Derive primitive manipulation skills from contact-state transitions. | Filtered contact graph |
| 03 | Semantic And Tool-Environment Constraints | 27-31 | Add semantic feasibility beyond physical contact. | Constraint gate |
| 04 | Skill-Agent Training And Control Laws | 32-42 | Explain how trainable agents and control laws realize transitions. | Policy surface |
| 05 | Grasp Skill Agents And Object Generalization | 43-54 | Show grasp as its own reusable skill family with object-shape transfer. | Grasp agent card |
| 06 | Errand Robot System Integration | 55-57 | Integrate recognition, task models, skill agents, and humanoid execution. | Errand system map |
| 07 | Historical Motivation And Essence Extraction | 58-64 | Reframe LfO historically and define essence as state transition. | State transition `T` |
| 08 | State Spaces Across Domains | 65-70 | Generalize state transitions across contact, mating, knots, and dance. | Domain-state atlas |
| 09 | Factorization, Transfer, And Final Synthesis | 71-77 | Compare imitation and LfO, explain transfer, limitations, and final takeaway. | Final architecture |

## Continuity Rules

- The final object of chapter `N` must appear in the first 10 seconds of chapter `N+1`.
- Chapters should not restart from a blank conceptual slate; they should re-anchor with the handoff object and then extend it.
- Each chapter has exactly one central thesis and each beat has exactly one full-sentence takeaway headline.
- Slide coverage is conceptual, not visual. Every slide contributes an idea, constraint, example, or summary role, but no full-slide screenshot is used.
- Later Manim scenes should use `MovingCameraScene`, `from manim import *`, ManimCE APIs only, vector redraws only, and low-quality preview before medium rendering.

## Visual Grammar

V5 uses a V4-style visual mathematical derivation on a black background:

- Persistent research canvas rather than slide-like page replacement.
- Thin state-transition edges, contact graphs, matrices, braces, axes, and interface boundaries.
- `Tex` / `MathTex` for content typography because MacTeX is installed.
- Avenir Next for takeaway titles only.
- Chapter progress rail visible but quiet.
- No more than two accent colors per beat.
- No screenshots, PDF crops, decorative motion, neon effects, scanlines, or copied slide layouts.

## Scoring Strategy

- Avoid content deductions by mapping every slide 1-77 exactly once in `deck_map.md`.
- Avoid ambiguity deductions by placing definitions in narration before symbols are reused.
- Avoid timing deductions by using chapter-level videos with coverage-first pacing instead of one overlong video.
- Target subtitle bonus with English narration and chapter-level `subtitles.srt` files.
- Target outstanding contribution by using a connected series architecture with chapter handoffs, not isolated video fragments.

## MIT CommKit Compliance

- Start each chapter with the larger motivation for that chapter before technical detail.
- Connect every mechanism to cross-environment or cross-hardware generalization.
- Interpret examples as evidence for the thesis, not as isolated demonstrations.
- One visual beat communicates one message.
- Beat titles stand alone as takeaway sentences.
- On-screen text supports visuals; details live in narration and subtitles.
- Limitations appear before the final synthesis.
