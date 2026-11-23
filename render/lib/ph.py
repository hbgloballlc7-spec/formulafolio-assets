"""Shared photo layer: real photography with slow Ken Burns, graded toward the Folio palette."""
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
from functools import lru_cache
import numpy as np

from base import KIT
import os
STOCK = os.path.join(KIT, 'photos') + '/'
AI = {}


@lru_cache(None)
def src(key):
    p = STOCK + key + '.jpg'
    im = Image.open(p).convert('RGB')
    # gentle grade: slight desaturation + warm-paper lift for one cohesive look
    im = ImageEnhance.Color(im).enhance(0.88)
    arr = np.asarray(im).astype(np.float32)
    tint = np.array([238, 236, 228], np.float32)
    arr = arr * 0.94 + tint * 0.06
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8))

def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def cover(key, w, h, p=0.0, focus=(0.5, 0.5), z0=1.0, z1=1.07):
    """Crop `key` to w x h at zoom interpolated by p in [0,1], centered on focus."""
    im = src(key); sw, sh = im.size; p = max(0.0, min(1.0, p))
    base = max(w / sw, h / sh); z = z0 + (z1 - z0) * p
    cw, ch = w / (base * z), h / (base * z)
    cx = min(max(focus[0] * sw, cw / 2), sw - cw / 2); cy = min(max(focus[1] * sh, ch / 2), sh - ch / 2)
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    return im.resize((w, h), Image.LANCZOS, box=box, reducing_gap=2.0)

def schedule(t, items, end, fade=0.7):
    """items: list of (start_time, key, focus). Returns list of (key, focus, alpha, progress)."""
    out = []
    for i, (t0, key, foc) in enumerate(items):
        t1 = items[i + 1][0] if i + 1 < len(items) else end
        if t < t0 - 0.01 or t > t1 + fade: continue
        a = 1.0 if i == 0 else ease((t - t0) / fade)
        p = (t - t0) / max(1.0, (t1 + fade) - t0)
        out.append((key, foc, a, max(0, min(1, p))))
    return out

def panel(im, box, t, items, end, cap=True):
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    layers = schedule(t, items, end)
    base = None
    for key, foc, a, p in layers:
        fr = cover(key, w, h, p, foc)
        base = fr if base is None or a >= 1 else Image.blend(base, fr, a)
    if base is None: return None
    im.paste(base, (x0, y0))
    return layers[-1][0] if layers else None

def vignette_bottom(im, box, strength=0.55, color=(16, 19, 21)):
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    g = np.linspace(0, 1, h) ** 1.6 * strength
    a = (np.repeat(g[:, None], w, 1) * 255).astype(np.uint8)
    ov = Image.new('RGB', (w, h), color)
    im.paste(ov, (x0, y0), Image.fromarray(a, 'L'))

def vignette_top(im, box, strength=0.5, color=(16, 19, 21)):
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    g = (1 - np.linspace(0, 1, h)) ** 1.8 * strength
    a = (np.repeat(g[:, None], w, 1) * 255).astype(np.uint8)
    im.paste(Image.new('RGB', (w, h), color), (x0, y0), Image.fromarray(a, 'L'))
