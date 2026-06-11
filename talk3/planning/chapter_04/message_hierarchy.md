# Chapter 04 Message Hierarchy

## Audience type

Academic robotics.

## Presenter purpose

Explain how valid state transitions become executable skill agents through dimensions, control laws, and RL training.

## Central thesis

Skill agents realize symbolic transitions by learning feedback policies over contact dimensions, admissible directions, and task parameters.

## Supporting claims

1. RL training turns a valid transition request into a reusable policy.
2. Maintain, detach, and constraint dimensions describe contact-state change.
3. Gaussian-sphere direction structure provides control-law geometry.
4. Drawer, door, wipe, place, and insert agents are instances of the same feedback-agent idea.

## Final takeaway

The skill library is executable because each symbolic transition is decoded into a feedback control law.

## Details to omit

- Numerical RL hyperparameters.
- Full plots or slide-specific training tables.
- Wiping as a central example; it appears only as one policy in the family.

## Terms that need visual explanation

- RL training
- Maintain dimension
- Detach dimension
- Constraint dimension
- Gaussian sphere
- Feedback policy

## MIT CommKit checklist

- Begins from Chapter 03's valid transition target.
- Defines dimensions before equations/control laws.
- Interprets examples as policy family evidence.
- Ends with policy surface handoff to grasp chapter.

