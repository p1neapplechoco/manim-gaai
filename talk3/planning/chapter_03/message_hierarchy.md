# Chapter 03 Message Hierarchy

## Audience type

Academic robotics.

## Presenter purpose

Show why physical feasibility is insufficient: tool use and environment interaction also require semantic constraints.

## Central thesis

A skill agent should pass both a physical constraint gate and a semantic constraint gate before execution.

## Supporting claims

1. Tool-environment common sense determines whether an action is appropriate.
2. Semantic constraints can be extracted from observation, especially task videos.
3. Semantic agents extend the current library beyond contact-only manipulation.
4. Library coverage is an explicit limitation, not an implementation detail.

## Final takeaway

LfO execution is constrained by physics and meaning; both gates shape which skill is valid.

## Details to omit

- Full cooking-video visual details.
- Exhaustive current library inventory.
- Any claim that semantic extraction is solved universally.

## Terms that need visual explanation

- Tool-environment common sense
- Physical constraint
- Semantic constraint
- Semantic manipulation agent
- Library coverage

## MIT CommKit checklist

- Begins from Chapter 02's filtered physical graph.
- Shows why a physically valid edge can still fail.
- Connects semantic constraints to generalist behavior.
- Ends with a constraint gate that becomes the training target in Chapter 04.

