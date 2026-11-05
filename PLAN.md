# aguywithascarf.com — the core AGWAS site

Plan, 31 October 2026. Phase 1: visual system and information architecture, for Carlo to pick.
Phase 2 (build) starts after the pick. Mock of the recommended direction in `mock/index.html`,
the three directions side by side in `mock/directions.html`.

## What exists today

| Property | URL | Look | Stack |
|---|---|---|---|
| Sport experiences hub | dataviz.aguywithascarf.com | dark #070910, Helvetica Neue light/bold, radial gradient blobs, pill buttons, rounded cards | hand-written HTML, `releases.json` + `ver.js` feed every app's version badge |
| Ten sport apps | f1 · tennis · top5 · nfl · nba · nhl · elections · worldcupbracket · golf · athletics | dark, one accent colour each (in `releases.json`) | static, nightly Actions |
| Research hub | research.aguywithascarf.com | warm paper, Archivo + Archivo Narrow, orange four-bar mark, light only | static, `bump.py` versions |
| Course | b2b.aguywithascarf.com | warm paper, Source Serif 4 + Inter Tight + JetBrains Mono, dark-red italic, three-dash scarf mark | Next.js on Railway |
| YouTube Football Tracker | ytft.aguywithascarf.com | app, login-gated | separate |
| Newsletter | LinkedIn + aguywithascarf.substack.com | | 342 posts, 627k impressions in the 12 months to 26 Oct 2026 (local store) |
| Root | aguywithascarf.com, www | 301 → factory63.com | DNS at GoDaddy |
| Sister brands | art.carlodemarchis.it · torinoecultura.it | white, black Helvetica Bold | jinja2 `build.py` → `docs/` |

Two findings that shape the recommendation:

1. The professional AGWAS sites (course, research) already share a look: warm paper, a serif or a
   grotesk with a mono for labels, one accent, no decoration. The dataviz hub and the apps are the
   dark family. The root does not need a third look. It needs to be the parent of the light one and
   introduce the dark one.
2. The whole catalogue is already versioned and dated (365 releases across ten apps since 1 July
   2026, every research report stamped, every post dated). That is the proof of judgement the brief
   asks for, and no template has it. The design should show it instead of hiding it behind cards.

## Three directions

**A · The Ledger (recommended).** Warm paper `#f6f3ee`, ink `#161512`, one dark red `#8a1c1c`.
Source Serif 4 for headings and titles (the course's serif), Inter Tight for UI text, JetBrains Mono
for every number, date and version. Hairline rules, numbered sections (01 Work … 06 About), the
project list as a ledger: swatch, name, one line, version, last release, release count. Screens as
flat 1px-framed strips, no shadows, no rounded corners. The only ornaments: the three-dash scarf
mark already on the course site, and a ten-stripe "scarf" rule made of the ten app colours.
The hero's graphic is a release timeline drawn from `releases.json`, not a stock image. Motion:
underline on hover, nothing else. Mock: `mock/index.html`.

**B · The Index.** Swiss and monochrome. Archivo alone, using its width axis (expanded wordmark,
narrow labels), black on `#f2f2f0`, project colours only as small swatches. Closest to the art site
and Torino e Cultura. Risk: cold, reads as a design studio rather than an insider.

**C · The Tower.** The apps' dark `#070910`, Bricolage Grotesque + JetBrains Mono, no blobs. The
page is a chart (releases per week, posts per month). Risk: a dark portfolio with glowing accents is
the AI-template default of 2026, and it fights the light course and research sites it introduces.

Rejected for all three: gradient blobs, three-icon feature rows, pill buttons, drop shadows, stock
hero, testimonial carousels, animated counters.

## Information architecture (one page, anchors; sub-pages only where they earn it)

0. Masthead: mark + "A Guy With A Scarf", nav Work · Writing · Research · Course · About,
   "Carlo De Marchis · Turin".
1. Hero: positioning line, lede, release timeline, four stats (live apps, releases, LinkedIn
   reach with its date, episodes).
2. Latest: six dated lines across all families (app release, newsletter, episode, research),
   generated at build time from `releases.json` + the Substack archive API.
3. 01 Work: the ten experiences as a ledger + six screens; links to the hub and release notes.
   The hub keeps its job as the deep page for the family; the root promotes it.
4. 02 Writing: newsletter (LinkedIn + Substack, latest four), the conversations (episodes), the
   book.
5. 03 Research: the three reports, dated.
6. 04 Course: b2b, with its screenshot.
7. 05 Tools: YouTube Football Tracker.
8. 06 About: portrait, bio in Carlo's words (the course's "Who am I" paragraph), the advisory
   disclosure inline (Dolby OptiView, Mercury Intermedia), the two non-AGWAS brands, contact via
   LinkedIn.
9. Footer: sitemap of every AGWAS domain + the usual non-affiliation note.

Sub-sites linking back: each app's top-bar brand link and the hub's "A guy with a scarf" link
point to the root; the research hub and the course get a one-line "Part of A Guy With A Scarf"
in their mastheads. `ver.js` already runs on every app, so a root link can ride on it with no
per-app deploy if wanted.

## Build (Phase 2, after the pick)

- `agwas-site/`: `build.py` (jinja2 + Pillow, same pattern as the sister sites), `site.json`,
  `templates/`, `static/`, `docs/` for GitHub Pages, repo `carlodemarchis-stack/agwas-site`.
- Data in: `../dataviz/releases.json` (versions, dates, colours, counts), Substack archive API
  (latest posts and episodes), `../linkedin-posts/posts.sqlite` (reach figures, with the capture
  date printed), the research hub's `version-log.json`.
- Images: fresh 2400px screenshots of every live app (headless Chrome with `?noumami`, alarm-
  wrapped), WebP at 1600/1000/600, og image 1200×630.
- Umami: new website id for `aguywithascarf.com`, opt-out line in the tag, added to
  `umami-tools/website_ids.json` and `targets.py`.
- Canonical + og/twitter tags, sitemap, 404, README. CNAME only once the domain is decided.
- Verified at desktop and phone widths in the browser pane; screenshots to Carlo.

## Open questions for Carlo

1. **Domain.** Root and www 301 to factory63.com today. Should the root become this site (Carlo
   changes the GoDaddy record, Pages gets the CNAME), or does Factory63 keep it and this lives
   at, say, home. or www.? Nothing touches DNS until this is answered.
2. **Direction** A, B or C, or A with changes.
3. **Mark.** Keep the course's three-dash scarf as the AGWAS mark (as in the mock), or the research
   hub's four bars, or a new one.
4. **Episodes.** Where do they live (YouTube channel URL, Substack podcast) and is "61 conversations"
   the right count to print?
5. **Book link** on Amazon, and whether Factory63 (the company) is named on the About block.
6. **Tooling line.** Say that the experiences are built with AI coding tools, or leave it out.
