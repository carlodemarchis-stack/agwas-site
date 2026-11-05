# AGWAS brand candidates (study, 2026-11-05)

Candidate marks from the logo and identity study. **Not wired into any page or build.**
Study artifact: https://claude.ai/artifact/XqpjF1xRii9ooehZFaY6BW

Carlo's framing (2026-11-05): the brand is **sports media, digital and AI**; the scarf is an accident. The
colours stay (they are what the photo and the existing favicons share) but they mean data and order, not cloth.

Recommended direction (Carlo's idea, 2026-11-05): **the dissolve**. Four horizontal bars in the scarf
colours (sand, turquoise, cobalt, red), solid at the left, breaking into particles toward the right: the
broadcast becoming data. No letter, no pictogram. Name "A Guy With A Scarf", Helvetica Neue 500.
Dropped on the way: sash (first pass), rounded G (too close to Google), typographic G, bracket / tactics /
lanes / formation pictograms (clip art). All kept under `alt/`.

Palette: Sand #E3A95F · Turquoise #1FA6BD · Cobalt #2D6FD2 · Red #D7442B · Navy #181D33 · Ink #111111 ·
Paper #FFFFFF · Night #070910. Cobalt is the text/link accent that holds on white (4.9:1) and night (4.1:1).

| File | Use |
|---|---|
| `dissolve.svg` | **Recommended favicon.** Four bars → particles, ink tile, rx 7. |
| `dissolve-paper.svg`, `-navy.svg`, `-bare.svg`, `-pixels.svg` | Paper tile, navy tile, no tile, square particles. |
| `mark-dissolve.svg` | Masthead tile mark, 4 px corners. |
| `mark-dissolve-wide.svg`, `-wide-drift.svg` | Wide mark (120×32 viewBox) for mastheads, credit lines, OG images. |
| `apple-touch-icon-dissolve.svg` | Square tile for iOS; export to PNG. |
| `alt/g/rounded-g.svg` | **Recommended favicon.** Ring + tail, four colours, ink tile, rx 7. |
| `alt/g/rounded-g-3.svg` | Same, three colours (no red). |
| `alt/g/rounded-g-segments.svg`, `-segments-3.svg` | Gaps between the segments: the live / loading state. |
| `alt/g/rounded-g-paper.svg`, `-navy.svg`, `-bare.svg`, `-bare-3.svg` | Paper tile, navy tile, no tile. |
| `alt/g/mark-rounded-g.svg`, `mark-rounded-g-3.svg` | Masthead mark, 4 px corners. |
| `alt/g/apple-touch-icon-rounded-g.svg` | Square tile for iOS; export to PNG. |
| `alt/g/favicon-g.svg` | Helvetica Neue Bold capital G cut from the scarf print (diagonal sand / turquoise / cobalt / brown / red), ink tile. The outline is the system font's glyph, converted to a path with fontTools. |
| `alt/g/favicon-g-paper.svg`, `-quiet.svg`, `-navy.svg`, `-bare.svg` | Paper tile; sand letter with two bands only; navy tile; no tile. |
| `alt/g/mark-g.svg`, `alt/g/apple-touch-icon-g.svg` | Masthead mark (4 px corners) and 180 px touch icon. |
| `favicon-scarf.svg` | 32 px tile, ink / sand band / turquoise + cobalt stripes. **Recommended favicon.** |
| `favicon-scarf-inverse.svg` | Sand tile, ink band. |
| `favicon-scarf-navy.svg` | Navy (sweater) tile. |
| `favicon-scarf-print.svg` | Full print, scarf fills the frame, no tile. |
| `mark-scarf.svg`, `mark-scarf-on-sand.svg` | Masthead mark, 4 px corners. |
| `apple-touch-icon-scarf.svg` | 180 px, square corners; export to PNG before wiring. |
| `favicon-sash.svg` | 32 px tile, ink tile / white sash. Default `<link rel="icon">`. |
| `favicon-sash-adaptive.svg` | Same, tile inverts with `prefers-color-scheme` (Chrome, Firefox). |
| `favicon-sash-inverse.svg` | White tile / ink sash, the dark-apps variant. |
| `apple-touch-icon-sash.svg` | 180 px, square corners; export to PNG before wiring. |
| `mark-sash.svg`, `mark-sash-on-dark.svg` | Masthead mark, 4 px corners, 20–28 px next to the name. |
| `alt/favicon-bands*.svg`, `alt/favicon-loop*.svg` | Directions 2 and 3, kept for comparison. |

Geometry, rounded G (viewBox 0 0 32 32): ring centre (15.5, 13.5), r 7.5, open from +38° to −38° on the
right, stroke 4.4 round caps (segments build: 3.8 butt, 1.6 gaps); tail from the lower ring end to
(x−3.2, 28.5). Segments are `stroke-dasharray="0 <start> <len> 300"` overlays on the same arc.

Geometry, sash (viewBox 0 0 32 32): tile `rx=7`; band = stroke 12 along `M-6 38 L38 -6`, clipped to
the tile; scarf stripes = same path, turquoise `stroke-dasharray="0 22 4 100"` and cobalt
`"0 29 4 100"` (Bordeaux version: `"0 22 4 3 4 100"`).

Geometry, dissolve (viewBox 0 0 32 32): bars h 4.2 at y 6.5 / 12.8 / 19.1 / 25.4, solid x 4→15, rounded ends;
particles from x 15 to 29.5 on a 0.9 grid, 2 per column, radius 1.25→0.3, density 1.0→0.05, vertical
jitter grows with x but stays in the lane (spread 0.9 × bar height). Deterministic PRNG seed 5. Generator in
the study's scratchpad (`pt2/` builder); re-run with other seeds for alternates.
