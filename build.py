#!/usr/bin/env python3
"""Render aguywithascarf.com into docs/ (GitHub Pages).

  python3 build.py               full build (image derivatives are cached by source hash)
  python3 build.py --no-images   template-only rebuild

Reads site.json (settings, links, numbers), content.json (every line of copy) and the hub's
../dataviz/releases.json (per-app versions and the release count). Images in sources/ become
WebP at four widths plus a JPEG og image. Needs python3 with jinja2 and Pillow.
"""
import datetime
import hashlib
import json
import os
import shutil
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
IMG = os.path.join(DOCS, "img")
SRC = os.path.join(ROOT, "sources")
SIZES = {"xl": 2000, "l": 1400, "m": 900, "s": 540}
WEBP_QUALITY = 82
NO_IMAGES = "--no-images" in sys.argv
Image.MAX_IMAGE_PIXELS = None

SITE = json.load(open(os.path.join(ROOT, "site.json")))
CONTENT = json.load(open(os.path.join(ROOT, "content.json")))


# ---------------------------------------------------------------- releases (from the hub)
def releases():
    path = os.path.abspath(os.path.join(ROOT, SITE["releases_json"]))
    d = json.load(open(path))
    apps, total, first = {}, 0, None
    for a in d["apps"]:
        total += len(a["releases"])
        for r in a["releases"]:
            dt = datetime.date.fromisoformat(r["date"])
            first = dt if first is None or dt < first else first
        latest = a["releases"][0]
        apps[a["id"]] = {"version": latest["version"], "date": latest["date"], "n": len(a["releases"]), "name": a["name"]}
    return {"apps": apps, "total": total, "count": len(d["apps"]),
            "since": first.strftime("%-d %B %Y"), "updated": d.get("updated", "")}


# ---------------------------------------------------------------- images
def load_source(path):
    im = ImageOps.exif_transpose(Image.open(path))
    return im.convert("RGB") if im.mode != "RGB" else im


def derive(name):
    """sources/<name>.jpg -> docs/img/<name>-<size>.webp for every size (cached by source hash)."""
    src = os.path.join(SRC, name + ".jpg")
    if not os.path.exists(src):
        raise SystemExit(f"missing source image: {src}")
    stamp = os.path.join(IMG, name + ".hash")
    h = hashlib.md5(open(src, "rb").read()).hexdigest()
    outs = {k: os.path.join(IMG, f"{name}-{k}.webp") for k in SIZES}
    if os.path.exists(stamp) and open(stamp).read() == h and all(os.path.exists(p) for p in outs.values()):
        im = Image.open(src)
        return {"w": im.size[0], "h": im.size[1]}
    im = load_source(src)
    w, h0 = im.size
    for k, side in SIZES.items():
        out = im.copy()
        if out.size[0] > side:
            out.thumbnail((side, int(side * h0 / w) + 1), Image.LANCZOS)
        out.save(outs[k], "WEBP", quality=WEBP_QUALITY, method=5)
    open(stamp, "w").write(h)
    return {"w": w, "h": h0}


IMAGES = {}


def pic(name, alt="", cls="", sizes="100vw", eager=False, pos=None):
    """<img> with a WebP srcset. `sizes` is the CSS sizes attribute."""
    meta = IMAGES.get(name)
    if meta is None:
        meta = IMAGES[name] = derive(name) if not NO_IMAGES else {"w": 1600, "h": 1000}
    srcset = ", ".join(f"/img/{name}-{k}.webp {min(side, meta['w'])}w" for k, side in SIZES.items())
    style = f' style="object-position:{pos}"' if pos else ""
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return Markup(f'<img src="/img/{name}-l.webp" srcset="{srcset}" sizes="{sizes}" width="{meta["w"]}" '
                  f'height="{meta["h"]}" alt="{alt}"{" class=" + chr(34) + cls + chr(34) if cls else ""}{style} {load}>')


def og_image():
    """1200x630 JPEG: the hero photo with a black bar carrying the name."""
    out = os.path.join(DOCS, "og.jpg")
    im = load_source(os.path.join(SRC, "hero.jpg"))
    w, h = im.size
    tw, th = w, int(w * 630 / 1200)
    top = int((h - th) * 0.35)
    im = im.crop((0, top, tw, top + th)).resize((1200, 630), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    try:
        f1 = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 54)
        f2 = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
    except OSError:
        f1 = f2 = ImageFont.load_default()
    lines = [("A Guy With A Scarf", f1), ("Carlo De Marchis · Sports and media technology, from the vendor side", f2)]
    y = 630 - 60
    for text, f in reversed(lines):
        bbox = d.textbbox((0, 0), text, font=f)
        tw_, th_ = bbox[2] - bbox[0], bbox[3] - bbox[1]
        y -= th_ + 22
        d.rectangle([48, y - 10, 48 + tw_ + 36, y + th_ + 14], fill=(17, 17, 17))
        d.text((66, y - bbox[1]), text, font=f, fill=(255, 255, 255))
        y -= 6
    im.save(out, "JPEG", quality=86)


# ---------------------------------------------------------------- render
def main():
    os.makedirs(IMG, exist_ok=True)
    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")),
                      autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)
    env.globals.update(pic=pic, site=SITE, content=CONTENT, links=SITE["links"], numbers=SITE["numbers"],
                       base=SITE["base_url"], rel=releases(), year=datetime.date.today().year,
                       built=datetime.date.today().isoformat())
    env.filters["safe_html"] = lambda s: Markup(s)
    WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
    env.filters["words"] = lambda n: WORDS[n] if 0 <= int(n) < len(WORDS) else str(n)
    work_by_id = {w["id"]: w for w in CONTENT["work"]}
    env.globals["work_strip"] = [work_by_id[i] for i in CONTENT["work_strip"]]

    if not NO_IMAGES:
        derive("hero-portrait")          # referenced by the <picture> source, not through pic()
    pages = {"index.html": ("index.html", "home"), "stage/index.html": ("stage.html", "stage"),
             "brand/index.html": ("brand.html", "brand"), "404.html": ("404.html", "404")}
    for out, (tpl, page) in pages.items():
        html = env.get_template(tpl).render(page=page)
        path = os.path.join(DOCS, out)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").write(html)

    for f in os.listdir(os.path.join(ROOT, "static")):
        src = os.path.join(ROOT, "static", f)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(DOCS, f), dirs_exist_ok=True)
        else:
            shutil.copy(src, os.path.join(DOCS, f))
    if not NO_IMAGES:
        og_image()
    open(os.path.join(DOCS, ".nojekyll"), "w").close()
    open(os.path.join(DOCS, "CNAME"), "w").write(SITE["domain"] + "\n")
    with open(os.path.join(DOCS, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in ("/", "/stage/", "/brand/"):
            f.write(f"  <url><loc>{SITE['base_url']}{u}</loc></url>\n")
        f.write("</urlset>\n")
    open(os.path.join(DOCS, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE['base_url']}/sitemap.xml\n")
    n = sum(len(fs) for _, _, fs in os.walk(DOCS))
    print(f"built {len(pages)} pages, {len(IMAGES)} images x {len(SIZES)} sizes, {n} files in docs/")


if __name__ == "__main__":
    main()
