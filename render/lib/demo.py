"""Motion demo reel (16:9): AI video b-roll + living photo + animated label scan, cut to Deanne narration.

python demo.py --clips drop.mp4 portrait.mp4 cream.mp4 forearm.mp4 --audio video1-final.mp4 --out demo.mp4
"""
import argparse, subprocess, os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base import *
import ph

W, H, FPS = 1920, 1080, 30

def frames_of(path, n):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    last = None
    for i in range(n):
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            yield last if last is not None else Image.new('RGB', (W, H), PAPER); continue
        last = Image.frombuffer('RGB', (W, H), b); yield last
    p.kill()

def chrome(c, label, a=1.0, dark=True):
    col = (240, 240, 236) if dark else MUTED
    c.text((80, 56), "THE FORMULA FOLIO", sans(24, "SemiBold"), col, a)
    c.text((W - 80, 56), label.upper(), sans(24, "Medium"), col, a, "ra")

def scrim(im, strength=0.55):
    ph.vignette_bottom(im, (0, 520, W, H), strength); ph.vignette_top(im, (0, 0, W, 220), 0.45)

def tag(c, txt, a):
    c.text((W - 30, H - 34), txt, sans(18), (240, 240, 236), 0.8 * a, "ra")

def seg_clip(path, dur, label, kicker, line, credit="AI-generated video"):
    n = round(dur * FPS)
    for i, fr in enumerate(frames_of(path, n)):
        t = i / FPS; im = fr.copy(); scrim(im)
        c = Canvas(W, H); c.im = im; c.redraw()
        chrome(c, label)
        a = prog(t, 0.4, 0.6) * (1 - prog(t, dur - 0.5, 0.5))
        c.text((80, 800), kicker.upper(), sans(30, "SemiBold"), (230, 170, 98), a)
        c.text((76, 846), line, bod(92, "700-normal"), (250, 250, 246), a)
        tag(c, credit, 1)
        yield c.im

def seg_living_photo(key, dur, label, kicker, line):
    """Living photo: slow push + parallax drift + window-light sweep + floating dust."""
    n = round(dur * FPS); rng = random.Random(7)
    dust = [(rng.random() * W, rng.random() * H, rng.uniform(1.5, 4), rng.uniform(8, 30), rng.random() * 6.28) for _ in range(70)]
    for i in range(n):
        t = i / FPS; p = t / dur
        im = ph.cover(key, W, H, p, (0.5 + 0.03 * math.sin(p * 2), 0.48), 1.0, 1.12).convert('RGB')
        # light sweep
        sweep = Image.new('L', (W, H), 0); d = ImageDraw.Draw(sweep)
        x = -600 + p * (W + 1200)
        d.polygon([(x, 0), (x + 380, 0), (x - 220, H), (x - 600, H)], fill=70)
        sweep = sweep.filter(ImageFilter.GaussianBlur(90))
        im.paste(Image.new('RGB', (W, H), (255, 236, 200)), (0, 0), sweep)
        dl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(dl)
        for (x0, y0, r, sp, ph0) in dust:
            yy = (y0 - sp * t) % H; xx = x0 + 18 * math.sin(t * 0.7 + ph0)
            al = int(120 * (0.5 + 0.5 * math.sin(t * 1.3 + ph0)))
            dd.ellipse((xx - r, yy - r, xx + r, yy + r), fill=(255, 246, 225, al))
        im = Image.alpha_composite(im.convert('RGBA'), dl.filter(ImageFilter.GaussianBlur(1.2))).convert('RGB')
        scrim(im)
        c = Canvas(W, H); c.im = im; c.redraw(); chrome(c, label)
        a = prog(t, 0.4, 0.6) * (1 - prog(t, dur - 0.5, 0.5))
        c.text((80, 800), kicker.upper(), sans(30, "SemiBold"), (230, 170, 98), a)
        c.text((76, 846), line, bod(92, "700-normal"), (250, 250, 246), a)
        tag(c, "Living photo · Unsplash", 1)
        yield c.im

def seg_label_scan(dur, label):
    """Animated label X-ray: ingredient list types on, scan line sweeps, matching rows light up."""
    n = round(dur * FPS)
    left = ["Water", "Ethoxydiglycol", "Ascorbic Acid", "+ the rest of the list"]
    right = ["Water", "Ethoxydiglycol", "Ascorbic Acid", "+ 8 more ingredients"]
    match = {0, 1, 2}
    bg = ph.cover('gelplates', W, H, 0.3).convert('RGB')
    bg = Image.blend(bg, Image.new('RGB', (W, H), PAPER), 0.8)
    for i in range(n):
        t = i / FPS
        c = Canvas(W, H); c.im = bg.copy(); c.redraw(); chrome(c, label, dark=False)
        c.text((W / 2, 130), "Label X-ray", bod(84, "700-normal"), INK, prog(t, 0.1), "ma")
        for col, (x, name, items, colr) in enumerate([(180, "SkinCeuticals · $185", left, OX), (1020, "Timeless · $27.95", right, TEAL)]):
            c.rect((x - 40, 250, x + 760, 880), fill=CARD, outline=RULE, width=2, r=18, a=prog(t, 0.2))
            c.text((x, 280), name, sans(32, "SemiBold"), colr, prog(t, 0.3))
            for k, ing in enumerate(items):
                tk = 0.6 + k * 0.22 + col * 0.1; y = 380 + k * 120
                a = prog(t, tk, 0.3)
                on = k in match and t > 3.2 + k * 0.35
                if k == 3: c.text((x, y), ing, sans(30, 'Medium'), MUTED, a); continue
                if on: c.rect((x - 16, y - 10, x + 736, y + 58), fill=TEAL_BG, r=10, a=prog(t, 3.2 + k * 0.35, 0.3))
                c.text((x, y), f"{k+1:>2}  {ing}", sans(44, "SemiBold" if on else "Medium"), TEAL if on else INK, a)
        # scan line
        sy = 340 + ((t - 1.8) / 1.6) * 640
        if 1.8 < t < 3.4:
            for xx in (140, 980):
                c.rect((xx, sy - 3, xx + 800, sy + 3), fill=TEAL, r=3, a=0.8)
        if t > 4.6:
            stamp(c, W / 2, 1010, "SAME FIRST THREE", t, 4.6, TEAL, 64, -3)
        yield c.im

def seg_end(dur, key):
    n = round(dur * FPS)
    for i in range(n):
        t = i / FPS
        im = ImageEnhance.Brightness(ph.cover(key, W, H, t / dur)).enhance(0.42).convert('RGB')
        c = Canvas(W, H); c.im = im; c.redraw()
        a = prog(t, 0.2, 0.6)
        c.text((W / 2, 380), "The Formula Folio", bod(120), (242, 242, 238), a, "ma")
        c.text((W / 2, 560), "We read the formula so you don’t overpay.", bod(56, "400-italic"), (230, 170, 98), a, "ma")
        c.text((W / 2, 1000), "MOTION DEMO · AI video + living photo + animated graphics", sans(22), (190, 196, 192), a, "ma")
        yield c.im

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--clips', nargs='+', required=True)
    ap.add_argument('--audio', required=True); ap.add_argument('--audio_start', type=float, default=0.0); ap.add_argument('--out', required=True)
    a = ap.parse_args(); drop, portrait, cream = a.clips[:3]; forearm = a.clips[3] if len(a.clips) > 3 else None
    plan = [seg_clip(drop, 4.2, "Formula vs. Formula", "SkinCeuticals C E Ferulic", "$185"),
            seg_clip(portrait, 4.4, "Formula vs. Formula", "If you use vitamin C", "This is for you"),
            seg_living_photo('drop', 4.0, "Formula vs. Formula", "Timeless 20% C + E Ferulic", "$27.95"),
            seg_label_scan(6.0, "Label X-ray")]
    if forearm: plan.append(seg_clip(forearm, 3.6, "The Folio Bench", "Your swatch, featured", "Film it. Send it.", "AI-generated video"))
    plan += [seg_clip(cream, 3.6, "The Folio Card", "The verdict", "Close, not identical."), seg_end(2.6, 'cream')]
    tmp = a.out + '.v.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    total = 0
    for seg in plan:
        for im in seg: p.stdin.write(im.tobytes()); total += 1
    p.stdin.close(); assert p.wait() == 0
    dur = total / FPS
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', str(a.audio_start), '-t', str(dur), '-i', a.audio, '-map', '0:v', '-map', '1:a',
                    '-af', f'afade=t=out:st={dur-1.5}:d=1.5', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', a.out], check=True)
    os.remove(tmp); print('ok', a.out, round(dur, 1))
