# Chapter 01 Storyboard

## Beat 1

Source: Slides 1-3.
Visual: A symbolic task goal appears at center, then branches to two tables and two robot silhouettes.
Narration intent: Motivate cross-environment and cross-hardware generalization.
On-screen text: "A generalist robot needs task intent that survives new settings."
Estimated time: 12s.
Transition: Branches collapse into a single observation strip.
Audience should understand: The problem is not single-task execution; it is reusable intent.

## Beat 2

Source: Slides 2-3.
Visual: A human trajectory is shown as a thin path, then replaced by an indirect task model card.
Narration intent: Define indirect mimicking.
On-screen text: "LfO copies the purpose of a demonstration, not its trajectory."
Estimated time: 13s.
Transition: The task model card moves into the encoder.
Audience should understand: LfO abstracts before execution.

## Beat 3

Source: Slides 5-11.
Visual: Language phrase and vision frames feed a GPT/VLM encoder.
Narration intent: Explain encoder output without model internals.
On-screen text: "The encoder turns observation into a compact task model."
Estimated time: 14s.
Transition: Card splits into two fields.
Audience should understand: Observation becomes structured task information.

## Beat 4

Source: Slide 7.
Visual: Instruction text highlights the verb and becomes a `what-to-do` field.
Narration intent: Show how primitives name the intended operation.
On-screen text: "`what-to-do` names the primitive action."
Estimated time: 12s.
Transition: Field waits while location evidence enters.
Audience should understand: The task model names an action, not a trajectory.

## Beat 5

Source: Slides 9-11.
Visual: Objects and surfaces receive affordance handles; one target parameter is selected.
Narration intent: Explain grounding.
On-screen text: "`where-to-do` grounds the action in objects and affordances."
Estimated time: 12s.
Transition: Completed task model moves toward library.
Audience should understand: The action is parameterized by the world.

## Beat 6

Source: Slides 4, 12-13, 15-17.
Visual: Skill chips for Pick, Bring, Place, Drawer, Door, Wipe are retrieved.
Narration intent: Establish the library as executable vocabulary.
On-screen text: "The skill library supplies `how-to-do` for each robot."
Estimated time: 15s.
Transition: One card branches to two robots.
Audience should understand: Execution is delegated to specialized agents.

## Beat 7

Source: Slide 14.
Visual: Same task card feeds two different robot silhouettes with different motion traces.
Narration intent: Interpret transfer as representation/execution separation.
On-screen text: "A task model can cross robot bodies because it is not a motor program."
Estimated time: 13s.
Transition: Robot traces fade; card remains.
Audience should understand: Task models are hardware independent at the symbolic level.

## Beat 8

Source: Slides 15-17.
Visual: The card points to an empty slot labeled "primitive skill vocabulary".
Narration intent: Set up Chapter 02.
On-screen text: "The next question is how to define the skill vocabulary."
Estimated time: 7s.
Transition: Handoff object freezes as `M = (what, where)`.
Audience should understand: Architecture requires a principled skill set.
