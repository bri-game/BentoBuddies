"""Compose the 1024x500 Play Store feature graphic from the game's own art atlas.

Play requires 1024x500, PNG/JPEG, no alpha channel.
"""
import json, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / 'assets/resources/art/v2'
OUT = ROOT / 'store-assets/feature-graphic.png'
W, H = 1024, 500
atlas = json.loads((ART / 'atlas.json').read_text())

def sprite(group, name):
    x, y, w, h = atlas[group][name]
    return Image.open(ART / f'{group}.png').convert('RGBA').crop((x, y, x + w, y + h))

def fit(im, height):
    return im.resize((round(im.width * height / im.height), height), Image.LANCZOS)

# Backdrop: top band of the in-game background (grass horizon + picnic cloth).
bg = Image.open(ART / 'background.png').convert('RGB')
bg = bg.resize((W, round(bg.height * W / bg.width)), Image.LANCZOS).crop((0, 0, W, H))
canvas = bg.copy()

# Cast bottom-aligned on the right, slightly overlapping like a group photo.
BASE = 470
for name, height, x in [('basket', 196, 486), ('rabbit', 172, 648), ('bear', 180, 744), ('frog', 172, 858)]:
    s = fit(sprite('food', name), height)
    canvas.paste(s, (x, BASE - s.height), s)

# Logo on the left, vertically centred.
logo = fit(sprite('logo', 'logo'), 300)
canvas.paste(logo, (46, (H - logo.height) // 2 - 10), logo)

OUT.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUT)  # RGB already -> no alpha channel
print(f'{OUT.relative_to(ROOT)}  {canvas.size}  mode={canvas.mode}')
