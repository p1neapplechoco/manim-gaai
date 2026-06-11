# Chapter 04 Storyboard

## Beat 1

Source: Slide 32.
Visual: Chapter 03 constraint gate emits a valid transition target, but the robot arm is still blank.
Narration intent: Separate validity from execution.
On-screen text: "A valid transition still needs a controller."
Estimated time: 11s.
Transition: Target enters RL loop.
Audience should understand: Constraints do not automatically create motion.

## Beat 2

Source: Slide 32.
Visual: RL loop: state -> action -> reward -> policy update.
Narration intent: Explain training at high level.
On-screen text: "RL trains a policy to realize the transition under feedback."
Estimated time: 11s.
Transition: Policy loop attaches to contact dimensions.
Audience should understand: Agents learn local execution.

## Beat 3

Source: Slide 33.
Visual: Maintain, detach, and constraint dimensions appear as three labeled axes.
Narration intent: Define the state variables that guide control.
On-screen text: "Contact dimensions describe what is maintained, detached, or constrained."
Estimated time: 12s.
Transition: Axes curve into a sphere.
Audience should understand: Dimensions summarize contact change.

## Beat 4

Source: Slide 34.
Visual: Gaussian sphere with admissible translation sectors.
Narration intent: Explain direction geometry without dense tables.
On-screen text: "Direction geometry turns dimensions into control choices."
Estimated time: 11s.
Transition: Selected sector becomes control vector.
Audience should understand: Direction choices are constrained by state.

## Beat 5

Source: Slide 35.
Visual: Dimension transition maps to a symbolic control law block.
Narration intent: Connect representation to executable law.
On-screen text: "Dimension transitions provide reusable control laws."
Estimated time: 12s.
Transition: Control law clones into examples.
Audience should understand: A transition type can reuse a controller.

## Beat 6

Source: Slides 36-38, 42.
Visual: Place and Insert panels show different target states using same decoding principle.
Narration intent: Ground abstract control laws in examples.
On-screen text: "Place and insert are examples of the same transition-to-policy decoding."
Estimated time: 12s.
Transition: Examples compress into skill library row.
Audience should understand: Different skills share a derivation pattern.

## Beat 7

Source: Slides 39-41.
Visual: Drawer, door, and wipe show distinct feedback loops.
Narration intent: Compare dynamic agents without centering one example.
On-screen text: "Drawer, door, and wipe agents differ in dynamics but share feedback execution."
Estimated time: 12s.
Transition: Feedback loops merge into a policy surface.
Audience should understand: Local feedback absorbs variation.

## Beat 8

Source: Slide 43.
Visual: Policy surface becomes a grasp-agent card with object-shape input.
Narration intent: Set up grasp chapter.
On-screen text: "The next chapter asks how grasping generalizes across object shape."
Estimated time: 8s.
Transition: Grasp card persists.
Audience should understand: Grasping is a specialized skill-agent family.

