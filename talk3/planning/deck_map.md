# V5 Deck Map

Every slide is covered exactly once as source material. Treatment is conceptual, not a promise to redraw the slide layout.

| Slide | Original topic | Chapter | Story role | Treatment | Visual translation | Coverage |
|---:|---|---|---|---|---|---|
| 1 | Agent Robotics | 01 | Larger motivation | Simplify | Generalist robot goal diverges into task representation problem | Covered |
| 2 | Learning-from-observation (LfO) | 01 | Define field | Merge | Observation becomes task model rather than copied motion | Covered |
| 3 | LfO indirect mimicking | 01 | Architecture principle | Keep | Indirect pipeline: observe -> encode -> execute | Covered |
| 4 | Pre-requisite for GPT-encoding | 01 | Skill-library prerequisite | Merge | Encoder requires reusable skill vocabulary | Covered |
| 5 | GPT-Encoder verbal + visual | 01 | Encoder input | Merge | Language and vision evidence enter same encoder | Covered |
| 6 | GPT-Encoder verbal + visual | 01 | Encoder continuation | Merge | Refinement of multi-modal encoding | Covered |
| 7 | ChatGPT to get what-to-do | 01 | What extraction | Keep | Text instruction becomes primitive action label | Covered |
| 8 | GPT-Encoder verbal + visual | 01 | Encoder continuation | Merge | Align visual observation with symbolic task fields | Covered |
| 9 | Affordance analyzer | 01 | Where extraction | Keep | Object/surface affordances produce parameters | Covered |
| 10 | VLM + LLM visual input only | 01 | Vision-only encoder | Keep | Demonstration frames produce `what` and `where` | Covered |
| 11 | Task models without verbal input | 01 | Evidence of encoding | Keep | Observation-only task model card | Covered |
| 12 | Skill agents retrieved from library | 01 | How execution starts | Keep | Task card queries skill library | Covered |
| 13 | Skill agent executes primitive actions | 01 | Feedback execution preview | Merge | Closed-loop agent preview, detailed later | Covered |
| 14 | Task models across robots | 01 | Transfer preview | Merge | Same task model branches to two robot bodies | Covered |
| 15 | Designing agent library | 01 | Library design question | Merge | Architecture ends by asking how to define skill set | Covered |
| 16 | Library of skill agents | 01 | Library criterion | Merge | Skill families approximate verbs and state transitions | Covered |
| 17 | Manipulation-skill agent | 01 | Bridge to chapter 2 | Keep | Manipulation skill card becomes handoff | Covered |
| 18 | Face contact relation | 02 | State representation | Keep | Contact state defines manipulation state variable | Covered |
| 19 | State of face contact | 02 | State semantics | Keep | Movable directions on Gaussian sphere | Covered |
| 20 | Kuhn-Tucker theory | 02 | Physical filtering | Simplify | Inequality constraints filter possible states | Covered |
| 21 | Possible transitions | 02 | Candidate graph | Keep | 7 states create 49 candidate edges | Covered |
| 22 | Physically possible transitions | 02 | Feasible graph | Keep | 49 edges reduce to 20 physical transitions | Covered |
| 23 | Examples from NC | 02 | Concrete edges | Merge | Bring/Place/Insert as labeled graph edges | Covered |
| 24 | Examples from PC | 02 | Concrete edges | Merge | Pick/Wipe and related PC transitions | Covered |
| 25 | Frequent YouTube transitions | 02 | Practical subset | Keep | 20 transitions reduce to 6 frequent tasks | Covered |
| 26 | Physical manipulation agents | 02 | Agent library | Keep | Translation and rotation task agents | Covered |
| 27 | Tool-env common sense | 03 | Motivation for semantics | Keep | Tool/environment relation can block a physical edge | Covered |
| 28 | Physical and semantic constraints | 03 | Constraint taxonomy | Keep | Two-layer gate: physical then semantic | Covered |
| 29 | Semantic constraints from cooking video | 03 | Demonstration evidence | Simplify | Cooking action requires role-aware object constraints | Covered |
| 30 | Semantic manipulation agents | 03 | Semantic agent library | Keep | Semantic agent chips extend physical library | Covered |
| 31 | Current agent library | 03 | Library inventory | Keep | Current library as coverage map and limitation | Covered |
| 32 | RL training of agents | 04 | Training principle | Keep | Transition request becomes RL training loop | Covered |
| 33 | Maintain/Detach/Constraint dimension | 04 | Contact dimension abstraction | Keep | Dimension change becomes control variable | Covered |
| 34 | Gaussian sphere and dimensions | 04 | Direction representation | Simplify | Admissible directions plotted on sphere | Covered |
| 35 | Dimension transition control laws | 04 | Control derivation | Keep | Dimension transitions generate control laws | Covered |
| 36 | Place U | 04 | Place agent | Merge | Place policy example in skill family | Covered |
| 37 | Insert | 04 | Insert agent | Merge | Insert policy example in skill family | Covered |
| 38 | S motion direction | 04 | Directional control | Merge | Motion direction as parameterized control law | Covered |
| 39 | Drawer-close PTG33 | 04 | RL-trained agent | Keep | Drawer-close feedback policy | Covered |
| 40 | Door opening PTG51 | 04 | RL-trained agent | Keep | Door-opening feedback policy | Covered |
| 41 | Wipe STG2 | 04 | RL-trained agent | Keep | Wipe as one policy, not series center | Covered |
| 42 | Insert NC-PR | 04 | Insert instance | Keep | Insert transition as policy output | Covered |
| 43 | Grasp-skill agent | 05 | Grasp chapter setup | Keep | Grasp as separate agent interface | Covered |
| 44 | Grasp types | 05 | Grasp vocabulary | Keep | Grasp type taxonomy simplified | Covered |
| 45 | Robotics grasp taxonomy | 05 | Prior taxonomy | Simplify | Taxonomy motivates task-purpose representation | Covered |
| 46 | From taxonomy to closure | 05 | Scientific abstraction | Keep | Closure condition replaces surface taxonomy | Covered |
| 47 | Three grasp agents prepared | 05 | Agent set | Keep | Three grasp agent chips | Covered |
| 48 | Contact-web based agent | 05 | End-to-end system | Keep | Contact-web pipeline | Covered |
| 49 | Super quadric | 05 | Shape representation | Keep | Object shape fitted as superquadric | Covered |
| 50 | Training CNN | 05 | Perception training | Keep | Image/shape to grasp parameter model | Covered |
| 51 | Reinforcement learning | 05 | Policy training | Keep | Grasp policy updates through reward | Covered |
| 52 | Various objects same grasp | 05 | Object variation | Keep | Same grasp intent over object distribution | Covered |
| 53 | Same agent grasps various shapes | 05 | Generalization evidence | Keep | Transfer across shape silhouettes | Covered |
| 54 | Passive-force and active-force agents | 05 | Force strategy | Keep | Two force-control modes | Covered |
| 55 | Errand robot project | 06 | System motivation | Keep | Whole errand task as integration target | Covered |
| 56 | Errand humanoid | 06 | Embodiment | Keep | Humanoid execution platform | Covered |
| 57 | Key components | 06 | System architecture | Keep | Recognition, task model, skill library, robot control | Covered |
| 58 | Transition slide | 07 | Reset marker | Simplify | Chapter divider: why LfO was needed historically | Covered |
| 59 | Diachronic discussion | 07 | Historical frame | Keep | Evolution from direct mimicry to essence extraction | Covered |
| 60 | Learning-from-observation | 07 | Core LfO contrast | Keep | Observation should preserve task, not path | Covered |
| 61 | How to obtain essence | 07 | Research question | Keep | Essence extraction question | Covered |
| 62 | Top-down LfO starting point | 07 | Method frame | Keep | Top-down decomposition from task purpose | Covered |
| 63 | Object and task recognition | 07 | Recognition layer | Keep | Recognize entities and task relation | Covered |
| 64 | Essence = state transition | 07 | Core abstraction | Keep | `T: s_t -> s_{t+1}` | Covered |
| 65 | Domains explore states | 08 | Domain generalization | Keep | Domain-state atlas intro | Covered |
| 66 | Polyhedral face-contact | 08 | Contact domain | Keep | Contact state panel | Covered |
| 67 | Machine-part mating | 08 | Assembly domain | Keep | Mating state panel | Covered |
| 68 | Knot topology | 08 | Topological domain | Keep | Knot state panel | Covered |
| 69 | Dance key pose and foot contact | 08 | Human motion domain | Keep | Key-pose state panel | Covered |
| 70 | Synchronic discussion | 08 | Cross-domain synthesis | Keep | Same transition principle across domains | Covered |
| 71 | Imitation learning vs LfO | 09 | Final contrast | Keep | Trajectory imitation contrasted with state transition | Covered |
| 72 | Symbolic teleoperation | 09 | Factorized architecture | Keep | Encoder/decoder split: what/where vs how | Covered |
| 73 | Cerebrum vs cerebellum | 09 | Reaction spectrum | Keep | Symbolic planning vs local adaptive control | Covered |
| 74 | Defense of only vision | 09 | Transfer constraint | Keep | Force is not observed; it is learned in execution | Covered |
| 75 | LfO and Piaget | 09 | Cognitive analogy | Simplify | Developmental analogy for internalized action schemas | Covered |
| 76 | Summary | 09 | Final takeaway | Keep | Restate factorization thesis | Covered |
| 77 | Publication and team | 09 | Attribution/closing | Keep | Source/team acknowledgment and final citation frame | Covered |

