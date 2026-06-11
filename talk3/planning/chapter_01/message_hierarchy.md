# Chapter 01 Message Hierarchy

## Audience type

Academic robotics.

## Presenter purpose

Explain why LfO starts from task intent rather than motion copying, and introduce the architecture that separates encoding from execution.

## Central thesis

An observed task becomes reusable only when it is encoded as `what-to-do` and `where-to-do`, then executed by robot-specific skill agents that supply `how-to-do`.

## Supporting claims

1. Generalist robots need task models that survive changes in bodies and environments.
2. GPT/VLM encoding extracts action primitives and grounded parameters from language and vision.
3. Skill-agent libraries are prerequisites, not afterthoughts, because task models must refer to executable primitives.
4. Cross-robot execution is possible when the task model does not contain joint trajectories.

## Final takeaway

LfO is an interface from observation to reusable task models, not a recorder of human motion.

## Details to omit

- Low-level network architecture for GPT/VLM models.
- Full slide layouts and screenshots.
- Detailed contact-state derivation, which is reserved for Chapter 02.

## Terms that need visual explanation

- Generalist agent
- Indirect mimicking
- `what-to-do`
- `where-to-do`
- `how-to-do`
- Skill-agent library

## MIT CommKit checklist

- Starts with generalist robot motivation.
- Connects encoder, task model, and skill library to transfer.
- Gives one message per beat.
- Uses takeaway headlines instead of noun labels.
- Ends with a handoff question: how should primitive skills be defined?

