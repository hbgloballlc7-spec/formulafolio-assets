import os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(KIT, 'fonts')
PAPER = (238, 240, 236); INK = (21, 25, 27); MUTED = (89, 98, 93); RULE = (198, 205, 200)
CARD = (248, 249, 246); TEAL = (31, 107, 100); AMBER = (168, 100, 26); OX = (138, 46, 46)
TEAL_BG = (214, 232, 228); AMBER_BG = (243, 226, 204); OX_BG = (240, 214, 211)
COLORS = {'ink': INK, 'teal': TEAL, 'amber': AMBER, 'ox': OX, 'muted': MUTED}
@lru_cache(None)
def bod(size, w="600-normal"): return ImageFont.truetype(os.path.join(FONTS, "bodoni-moda-latin-%s.woff" % w), size)
@lru_cache(None)
def sans(size, w="Regular"): return ImageFont.truetype(os.path.join(FONTS, "Inter-%s.otf" % w), size)
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x):
    x = clamp(x); return 1 - (1 - x) ** 3
def prog(t, t0, dur=0.5): return ease((t - t0) / dur)
class Canvas:
    def __init__(self, w, h, bg=PAPER):
        self.im = Image.new("RGB", (w, h), bg); self.d = ImageDraw.Draw(self.im, "RGBA")
    def redraw(self): self.d = ImageDraw.Draw(self.im, "RGBA")
    def text(self, xy, s, font, fill=INK, a=1.0, anchor="la", dy=0):
        if a <= 0: return
        x, y = xy; y += (1 - a) * 24 + dy
        self.d.text((x, y), s, font=font, fill=fill + (int(255 * a),), anchor=anchor)
    def rect(self, box, fill=None, outline=None, width=1, r=0, a=1.0):
        if a <= 0: return
        self.d.rounded_rectangle(box, radius=r, fill=fill + (int(255 * a),) if fill else None,
                                 outline=outline + (int(255 * a),) if outline else None, width=width)
    def line(self, pts, fill, width=2, a=1.0):
        if a > 0: self.d.line(pts, fill=fill + (int(255 * a),), width=width)
def stamp(c, cx, cy, txt, t, t0, color=OX, size=120, angle=-6):
    p = clamp((t - t0) / 0.35)
    if p <= 0: return
    sc = 1.6 - 0.6 * ease(p); f = bod(int(size), "700-normal")
    bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]; pad = 36
    layer = Image.new("RGBA", (tw + pad * 2, th + pad * 2 + 20), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([4, 4, layer.width - 5, layer.height - 5], radius=14, outline=color + (255,), width=8)
    ld.text((pad - bb[0], pad - bb[1] + 10), txt, font=f, fill=color + (255,))
    layer = layer.resize((max(1, int(layer.width * sc)), max(1, int(layer.height * sc))), Image.LANCZOS)
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    layer.putalpha(layer.split()[3].point(lambda v: int(v * ease(p * 1.5))))
    c.im.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer); c.redraw()
def wrap(s, font, maxw):
    words = s.split(); lines = []; cur = ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if font.getlength(t) <= maxw: cur = t
        else: lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines
