#!/usr/bin/env python3
"""LinkedIn image set for the site + brand launch: 1080x1350 portraits, one headline + one framed crop of the live page each.

  python3 social/make_launch.py            -> social/launch/01-cover.png … 06-channels.png (+ the crops in social/launch/crops/)

Source: shots/home-2026-11-09-1440x2.png (the live home page at 1440 CSS px, device scale 2). Crop boxes are CSS px
measured in the browser (getBoundingClientRect at 1440 wide); the script doubles them. Rendering: an HTML page per
image shot with headless Chrome, wrapped in a perl alarm because Chrome on this Mac can hang after writing the file.
"""
import os
import subprocess

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "shots", "home-2026-11-09-1440x2.png")
OUT = os.path.join(ROOT, "social", "launch")
CROPS = os.path.join(OUT, "crops")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1080, 1350

# name, (top, height) in CSS px at 1440 wide, headline, kicker
SLIDES = [
    ("02-hero", (0, 929), "One sentence, two menus: who I work with and on what.", "The home page"),
    ("03-vendor", (929, 1081), "Thirty-five years on the vendor side, and what I do with them now.", "About"),
    ("04-services", (2790, 790), "Seven services. Advisory to data experiences.", "Services"),
    ("05-data", (4600, 720), "Ten live sport data experiences, from official feeds, updated every night.", "Work"),
    ("06-channels", (5740, 700), "Every channel, every platform, one door: LinkedIn.", "Follow me"),
]

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;background:#fff;color:#111;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}}
.c{{width:{W}px;height:{H}px;box-sizing:border-box;padding:64px 0 0 64px;display:flex;flex-direction:column;position:relative;overflow:hidden}}
.top{{display:flex;align-items:center;justify-content:space-between;font-size:20px;color:#6b6b6b;padding-right:64px}}
.top b{{color:#111;font-weight:600}}
.top img{{height:28px;width:auto;display:block}}
.kick{{font-size:16px;letter-spacing:.14em;text-transform:uppercase;color:#2D6FD2;font-weight:600;margin:56px 0 14px}}
h1{{font-weight:700;font-size:54px;line-height:1.04;letter-spacing:-.035em;margin:0 0 44px;text-wrap:balance;padding-right:64px}}
.frame{{width:1140px;border:1px solid #e3e3e3;border-radius:14px 0 0 0;overflow:hidden;box-shadow:0 30px 60px -30px rgba(0,0,0,.35);background:#fff;flex:none}}
.bar{{height:36px;background:#f4f4f4;border-bottom:1px solid #e3e3e3;display:flex;align-items:center;padding:0 14px;gap:7px;font-size:13px;color:#6b6b6b}}
.bar i{{width:10px;height:10px;border-radius:50%;background:#d9d9d9;display:block}}
.bar span{{margin-left:10px}}
.frame img{{display:block;width:100%;height:auto}}
</style></head><body><div class="c">
<div class="top"><img src="file://{mark}" alt=""><span><b>aguywithascarf.com</b> · new site and mark</span></div>
<div class="kick">{kicker}</div>
<h1>{headline}</h1>
<div class="frame"><div class="bar"><i></i><i></i><i></i><span>aguywithascarf.com</span></div><img src="file://{crop}"></div>
</div></body></html>"""

COVER = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;background:#fff;color:#111;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}}
.c{{width:{W}px;height:{H}px;box-sizing:border-box;padding:96px 88px;display:flex;flex-direction:column;justify-content:space-between}}
.lock img{{width:560px;height:auto;display:block}}
h1{{font-weight:700;font-size:72px;line-height:1;letter-spacing:-.04em;margin:0 0 28px;text-wrap:balance}}
p{{font-size:26px;line-height:1.35;color:#333;margin:0;max-width:30ch}}
.url{{font-size:34px;font-weight:700;letter-spacing:-.02em;border-top:1px solid #e3e3e3;padding-top:28px}}
.url small{{display:block;font-size:18px;font-weight:400;color:#6b6b6b;margin-top:6px}}
</style></head><body><div class="c">
<div class="lock"><img src="file://{lockup}" alt="A Guy With A Scarf"></div>
<div><h1>A new home, and a mark.</h1><p>The newsletter, the conversations, the research, the course, the data experiences and the stage record, on one page.</p></div>
<div class="url">aguywithascarf.com<small>Live since 5 November 2026</small></div>
</div></body></html>"""


def shoot(html, out):
    page = out[:-4] + ".html"
    open(page, "w").write(html)
    subprocess.run(["perl", "-e", "alarm 60; exec @ARGV", CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                    "--user-data-dir=/tmp/claude-501/chrome-agwas-launch", "--force-device-scale-factor=1", f"--window-size={W},{H}",
                    f"--screenshot={out}", "file://" + page], capture_output=True)
    os.remove(page)
    print(out if os.path.exists(out) else f"FAILED {out}")


def main():
    os.makedirs(CROPS, exist_ok=True)
    src = Image.open(SRC)
    mark = os.path.join(ROOT, "docs", "brand", "agwas-mark-wide.svg")
    lockup = os.path.join(ROOT, "docs", "brand", "agwas-lockup-stacked-person.svg")
    shoot(COVER.format(W=W, H=H, lockup=lockup), os.path.join(OUT, "01-cover.png"))
    for name, (top, h), headline, kicker in SLIDES:
        crop = os.path.join(CROPS, f"{name}.png")
        src.crop((0, top * 2, src.width, (top + h) * 2)).save(crop, optimize=True)
        shoot(PAGE.format(W=W, H=H, mark=mark, crop=crop, headline=headline, kicker=kicker), os.path.join(OUT, f"{name}.png"))


if __name__ == "__main__":
    main()
