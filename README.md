# aguywithascarf.com

The root site of A Guy With A Scarf: Carlo De Marchis, advisor in sports and media technology.
One page plus a deep dive on moderation and speaking, served by GitHub Pages from `docs/`.

```
agwas-site/
├── build.py          renders docs/ with jinja2, resizes images with Pillow, writes og.jpg, sitemap, CNAME
├── site.json         settings: domain, Umami id, links, the numbers printed on the page and their date
├── content.json      every line of copy: hero pickers, bio, stages, services, channels, the stage page
├── templates/        base.html, index.html, stage.html, 404.html, _record.html (the stage record, shared)
├── static/           style.css, site.js (the hero rotation), favicon.svg → copied into docs/
├── sources/          photos and app screenshots at full size (JPEG)
└── docs/             the generated site, what GitHub Pages serves
```

## Build

```bash
python3 build.py              # full build, image derivatives cached by source hash
python3 build.py --no-images  # template-only rebuild
```

Needs the system python3 with jinja2 and Pillow. The release count and per-app versions come from
`../dataviz/releases.json`, so the hub repo must sit next to this one. Then:

```bash
git add -A && git commit -m "content: …" && git push
```

## Editing

- Copy lives in `content.json`. Numbers that can go stale (followers, subscribers, episode counts)
  live in `site.json` under `numbers`, with `as_of`; the footer prints the date.
- A new photo: drop a JPEG in `sources/`, reference it by name with `pic("name", ...)` in a template
  or by the `img` field in `content.json`. The build writes four WebP widths.
- The hero pickers: `content.json` → `picker.who`, `picker.what` (option → the line of copy) and
  `picker.tour` (the pairings the ten-second rotation walks through).
- Stage record: `content.json` → `stages` (live) and `air` (hosted formats). The home page folds it
  behind a toggle; `/stage/` shows it in full.

## Conventions

- Umami (self-hosted, `m.aguywithascarf.com`) on every page, with the `?noumami` opt-out line in the
  tag. Website id in `site.json`; also registered in `../umami-tools/website_ids.json` and `targets.py`.
- Canonical, Open Graph and Twitter tags on every page; `og.jpg` is 1200×630, generated from the hero.
- Domain: `aguywithascarf.com` (CNAME written by the build). `www` redirects to the bare domain.
- Copy follows the AGWAS writing standard: no dashes, numbers carry their date, first person only for
  judgement or something done.
