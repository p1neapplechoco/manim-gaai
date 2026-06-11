# Chapter 01 Video Outline

## Title

LfO Problem And Architecture

## Runtime target

1:35-1:50 for the implemented Chapter 01 cut. Coverage, clarity, and subtitle alignment take priority over forcing a longer runtime.

## Beat outline

| Beat | Time | Takeaway headline | Source slides | Visual core |
|---:|---:|---|---|---|
| 1 | 0:00-0:12 | A generalist robot needs task intent that survives new settings. | 1-3 | One task branches across environments and robot bodies |
| 2 | 0:12-0:25 | LfO copies the purpose of a demonstration, not its trajectory. | 2-3 | Direct replay fades into indirect task model |
| 3 | 0:25-0:39 | The encoder turns observation into a compact task model. | 5-11 | Language/vision evidence enters GPT/VLM encoder |
| 4 | 0:39-0:51 | `what-to-do` names the primitive action. | 7 | Instruction becomes action primitive |
| 5 | 0:51-1:03 | `where-to-do` grounds the action in objects and affordances. | 9-11 | Affordance analyzer outputs target parameters |
| 6 | 1:03-1:18 | The skill library supplies `how-to-do` for each robot. | 4, 12-13, 15-17 | Task model queries skill chips |
| 7 | 1:18-1:31 | A task model can cross robot bodies because it is not a motor program. | 14 | Same card branches to two robot silhouettes |
| 8 | 1:31-1:38 | The next question is how to define the skill vocabulary. | 15-17 | Handoff task card points to manipulation skill graph |

## Chapter handoff

End with a task model card `M = (what, where)` connected to an empty skill-library slot. Chapter 02 opens by asking which state transitions deserve to become primitive skills.
