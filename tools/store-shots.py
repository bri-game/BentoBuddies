"""Drive the release build on a device/emulator and capture Play Store screenshots.

Coordinates are in the 720x1280 design canvas; SHOW_ALL letterboxing is applied
via SCALE/OFFSET, computed from the device resolution.
"""
import subprocess, time, json, pathlib, os, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'store-assets' / 'screenshots'
ADB = os.environ.get('BENTO_ADB', 'adb')
SERIAL = os.environ.get('BENTO_SERIAL', 'emulator-5554')
PKG = os.environ.get('BENTO_PKG', 'bento.buddies.mediumbrain')
LEVELS = json.loads((ROOT / 'assets/resources/data/levels.json').read_text())['levels']

def adb(*a, binary=True):
    r = subprocess.run([ADB, '-s', SERIAL, *map(str, a)], check=True, stdout=subprocess.PIPE)
    return r.stdout if binary else r.stdout.decode(errors='replace')

W, H = (int(v) for v in adb('shell', 'wm', 'size', binary=False).strip().split(':')[1].strip().split('x'))
SCALE = min(W / 720, H / 1280)
OFFSET = (H - 1280 * SCALE) / 2

def tap(x, y, wait=.45):
    adb('shell', 'input', 'tap', round(x * SCALE), round(y * SCALE + OFFSET)); time.sleep(wait)

def shot(name, wait=1.2):
    time.sleep(wait); OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f'{name}.png').write_bytes(adb('exec-out', 'screencap', '-p')); print('  shot', name)

def alive():
    assert adb('shell', 'pidof', PKG, binary=False).strip(), 'game process died'

def restart(clear=False):
    adb('shell', 'am', 'force-stop', PKG)
    if clear: adb('shell', 'pm', 'clear', PKG)
    adb('shell', 'am', 'start', '-n', PKG + '/com.cocos.game.AppActivity'); time.sleep(14); alive()

def solve(n, fraction=1.0):
    """Play level n by tapping its stored solution. fraction<1 leaves it unfinished."""
    l = LEVELS[n - 1]
    c = min(108, 536 / l['w'], 372 / l['h'])
    bx = (720 - l['w'] * c) / 2; by = 357 + (372 - l['h'] * c) / 2
    pieces = l['pieces'][:max(1, round(len(l['pieces']) * fraction))]
    for i, p in enumerate(pieces):
        q = l['solution'][p['id']]
        tap(108 + i % 4 * 168, 880 + i // 4 * 126)       # pick from tray
        for _ in range(q['r']): tap(130, 1110)            # rotate
        tap(bx + (q['x'] + .5) * c, by + (q['y'] + .5) * c)  # place

def crop_all():
    """Play requires max dimension <= 2x min dimension; a 1080x2400 capture is 2.22
    and gets rejected. The game letterboxes its 720x1280 canvas, so cropping to the
    rendered content area yields a compliant 16:9 image with no empty bars."""
    from PIL import Image
    top, height = round(OFFSET), round(1280 * SCALE)
    for f in sorted(OUT.glob('*.png')):
        im = Image.open(f)
        if im.size != (W, H):
            continue
        im.crop((0, top, W, top + height)).convert('RGB').save(f)
        print(f'  cropped {f.name} -> {W}x{height}  ratio {max(W,height)/min(W,height):.2f}')
