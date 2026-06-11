# V5 Visual System

## Base Style

V5 uses a black academic derivation style: a research board that gradually accumulates task representations, graph filters, skill policies, and transfer conditions. The background is a user-approved pure black override so the series reads closer to V4's high-contrast derivation style.

## Required Tokens

The AGENTS.md design system remains authoritative for all non-background colors. `BG_PRIMARY = "#000000"` is an explicit user-approved override of the default AGENTS background token.

```python
BG_PRIMARY    = "#000000"
BG_SECONDARY  = "#1e293b"
BG_TERTIARY   = "#334155"
TEXT_PRIMARY  = "#f8fafc"
TEXT_SECONDARY = "#94a3b8"
TEXT_MUTED    = "#475569"
ACCENT_BLUE   = "#38bdf8"
ACCENT_PURPLE = "#a78bfa"
ACCENT_AMBER  = "#fbbf24"
ACCENT_GREEN  = "#34d399"
ACCENT_CORAL  = "#fb7185"
BORDER_COLOR  = "#334155"
```

## Typography

- Takeaway titles: `Text(..., font="Avenir Next", weight=BOLD, font_size=FONT_TITLE)`.
- Content labels: `Tex(...)` so labels use a TeX-style typeface and stay visually academic.
- Equations and symbols: `MathTex(...)`.
- No label below `FONT_CAPTION`.
- No more than two font sizes per beat: one title size and one internal label size.

## Color Semantics

| Concept | Color |
|---|---|
| Source observation, encoder input, task model source | `ACCENT_BLUE` |
| Skill agents, alternative mechanism, second concept | `ACCENT_PURPLE` |
| Key abstraction or selected transition | `ACCENT_AMBER` |
| Successful transfer or valid condition | `ACCENT_GREEN` |
| Failure, collision, invalid grounding, missing skill | `ACCENT_CORAL` |

Maximum two accent colors per beat. Color must never be the only encoding; pair it with text, geometry, line style, or symbol.

## Layout

- 16:9 frame, 1280x720, 30 FPS target.
- One title at top using `to_edge(UP, buff=0.5)`.
- Main derivation area centered below the title.
- Chapter progress rail at bottom: `01/09` through `09/09`, muted labels, current chapter in `TEXT_PRIMARY`.
- Use 12-column alignment mentally: left for evidence/input, center for abstraction, right for execution/output.
- Avoid dense rounded cards. Prefer graph nodes, equations, braces, boundary lines, and compact labels.

## Motion

- Reveal input before processing before output.
- Prefer `ReplacementTransform`, `TransformFromCopy`, `TransformMatchingTex`, `GrowArrow`, `LaggedStart`, and `Indicate`.
- Camera movement is reserved for state-space inspection, feedback loops, and final pullbacks.
- Static holds should not dominate. Later implementation should cap normal holds at `T_PAUSE_STD` and reserve `T_PAUSE_LONG` for chapter conclusions.

## Reusable Visual Components

- `takeaway_title(text)`.
- `chapter_progress(current, total=9)`.
- `handoff_object(name, symbol, color)`.
- `state_node(label)`.
- `transition_edge(source, target, label)`.
- `constraint_gate(label, pass_fail)`.
- `skill_agent_chip(name, family)`.
- `feedback_loop(goal, state, action, sensor)`.
- `bounded_tex(label, width, height)`.

## Anti-Patterns

- Full-slide screenshots or PDF crops.
- Bullet-list animation.
- More than two accents per beat.
- Long paragraphs on screen.
- Label shrinking below `FONT_CAPTION`.
- Unexplained equations or unexplained axes.
- Hard cuts that lose the handoff object.
