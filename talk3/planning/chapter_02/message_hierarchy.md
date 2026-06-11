# Chapter 02 Message Hierarchy

## Audience type

Academic robotics.

## Presenter purpose

Derive manipulation primitive actions from face-contact state transitions rather than from an arbitrary verb list.

## Central thesis

Primitive manipulation skills are meaningful because they are edges between physically valid contact states.

## Supporting claims

1. Face-contact relations define the manipulation state.
2. Kuhn-Tucker constraints filter possible transitions into physically possible transitions.
3. Practical skill libraries prioritize transitions that appear frequently in observed tasks.
4. Physical manipulation agents are grounded in this filtered transition structure.

## Final takeaway

The skill vocabulary is induced by state transitions: `49 possible -> 20 physical -> 6 frequent`.

## Details to omit

- Full Kuhn-Tucker derivation algebra.
- Dense transition tables.
- All individual transition labels beyond representative examples.

## Terms that need visual explanation

- Face-contact state
- Gaussian sphere
- Candidate transition
- Physically possible transition
- Frequent transition

## MIT CommKit checklist

- Begins from the skill-vocabulary question handed off by Chapter 01.
- Explains why contact state matters before showing transition counts.
- Interprets the counts as library design evidence.
- Ends with a filtered graph for Chapter 03.

