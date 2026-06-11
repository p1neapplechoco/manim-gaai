# V5 Subtitle Plan

## Policy

- Primary subtitles are English, matching the English narration script.
- Subtitles should be authored as `.srt` files per chapter and kept under each `planning/v5/chapter_XX/` directory.
- Manim renders should remain video-only unless audio/subtitle embedding is explicitly requested later.
- Future post-production can convert the `.srt` files to `.vtt` or generate Vietnamese translation from the English source.

## Timing Conventions

- Subtitle line duration: 3-7 seconds.
- Maximum two lines per subtitle block.
- Avoid showing equations before narration has defined them.
- Use spoken language, not slide bullet phrasing.
- Use `what-to-do`, `where-to-do`, and `how-to-do` consistently.
- Preserve symbol spacing in subtitles: `T: s_t -> s_{t+1}`, `M = (what, where)`.

## Naming Scheme

```text
planning/v5/chapter_01/subtitles.srt
planning/v5/chapter_02/subtitles.srt
...
planning/v5/chapter_09/subtitles.srt
```

Future rendered assets:

```text
outputs/v5/chapter01/Chapter01V5_medium.mp4
outputs/v5/chapter01/Chapter01V5.en.srt
```

## Sync Notes

- Narration anchors in `narration.md` are the source of truth.
- SRT timings are planning targets; final timings should be adjusted after low-quality render inspection.
- If a visual beat changes duration during implementation, update both narration anchors and subtitle blocks in the same commit.

