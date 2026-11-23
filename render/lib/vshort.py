"""The Formula Folio vertical Short renderer (house style).

Full-bleed real photography on top (slow Ken Burns, cross-fades per beat), the product/brand name large in the
header, one big serif statement per beat in the paper panel below, optional data visual, burned captions, and a
branded end card. Photos whose key starts with ai_ or spec_ are credited as AI/illustration.
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageEnhance
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base import *
import ph

W, H, FPS = 1080, 1920, 30
PH = 1160

def credit_for(key):
    if key.startswith('ai_'): return "AI-generated photo · labels by The Formula Folio"
    if key.startswith('spec_') or key == 'patentart': return "Photo: Unsplash · card by The Formula Folio"
    return "Photo: Unsplash"

def wrapc(c, cx, y, txt, f, col, a, maxw=940):
    lh = int(f.size * 1.18)
    for ln in wrap(txt, f, maxw): c.text((cx, y), ln, f, col, a, "ma"); y += lh
    return y

# ---------- data visuals ----------
def vis_bars(c, t, t0, y, a, v):
    rows = v['rows']; mx = max(r['value'] for r in rows); unit = v.get('unit', '')
    for k, r in enumerate(rows):
        aa = prog(t, t0 + r.get('at', 0.3 + k * 0.7)); yy = y + 10 + k * 170; col = COLORS[r.get('color', 'teal')]
        c.text((100, yy), r['label'], sans(34, "Medium"), INK, aa)
        c.rect((100, yy + 56, 700, yy + 114), fill=RULE, r=29, a=aa)
        ww = 600 * r['value'] / mx * ease(clamp((t - t0 - r.get('at', 0.3 + k * 0.7)) / 1.0))
        if ww > 6: c.rect((100, yy + 56, 100 + ww, yy + 114), fill=col, r=29, a=aa)
        c.text((990, yy + 34), r.get('text', f"{r['value']}{unit}"), bod(78, "700-normal"), col, aa, "ra")

def vis_chips(c, t, t0, y, a, v):
    x = 80; yy = y
    for k, w_ in enumerate(v['items']):
        fnt = sans(34, "SemiBold"); ww = fnt.getlength(w_) + 56
        if x + ww > W - 80: x = 80; yy += 92
        aa = prog(t, t0 + 0.4 + k * 0.5)
        c.rect((x, yy, x + ww, yy + 72), fill=CARD, outline=RULE, width=2, r=36, a=aa)
        c.text((x + 28, yy + 16), w_, fnt, INK, aa); x += ww + 18

def vis_stamp(c, t, t0, y, a, v):
    stamp(c, W / 2, y + 110, v['text'], t, t0 + v.get('at', 0.6), COLORS[v.get('color', 'ox')], v.get('size', 64), -4)

def vis_rank(c, t, t0, y, a, v):
    """Ingredient-position tracks: rows of {label, total, hi:[from,to], color}."""
    for k, r in enumerate(v['rows']):
        aa = prog(t, t0 + r.get('at', 0.3 + k * 0.8)); yy = y + 10 + k * 175; col = COLORS[r.get('color', 'teal')]
        c.text((100, yy), r['label'], sans(32, "Medium"), INK, aa)
        n = r['total']; x0, x1 = 100, 980; cw = (x1 - x0) / n
        for i in range(n):
            on = r['hi'][0] <= i + 1 <= r['hi'][1]
            c.rect((x0 + i * cw + 1, yy + 58, x0 + (i + 1) * cw - 1, yy + 108), fill=col if on else RULE, r=3, a=aa)
        c.text((x1, yy + 118), r.get('note', ''), sans(28, "SemiBold"), col, aa, "ra")

def vis_stat(c, t, t0, y, a, v):
    c.text((W / 2, y), v['big'], bod(150, "700-normal"), COLORS[v.get('color', 'teal')], prog(t, t0 + 0.3), "ma")
    if v.get('small'): wrapc(c, W / 2, y + 185, v['small'], sans(34, "Medium"), MUTED, prog(t, t0 + 0.6))

VIS = {'bars': vis_bars, 'chips': vis_chips, 'stamp': vis_stamp, 'rank': vis_rank, 'stat': vis_stat}

def frame(t, header, beats, total):
    c = Canvas(W, H)
    ph.panel(c.im, (0, 0, W, PH), t, [(b['t'], b['photo'], tuple(b.get('focus', (0.5, 0.5)))) for b in beats], total)
    ph.vignette_top(c.im, (0, 0, W, 520), 0.88); ph.vignette_bottom(c.im, (0, PH - 380, W, PH), 0.35); c.redraw()
    c.text((W / 2, 64), "THE FORMULA FOLIO", sans(36, "SemiBold"), (236, 238, 234), 0.95, "ma")
    hs = 104
    while bod(hs, "700-normal").getlength(header) > 1000 and hs > 64: hs -= 2
    c.text((W / 2, 118), header, bod(hs, "700-normal"), (252, 252, 248), 1.0, "ma")
    cur = [b for b in beats if b['t'] <= t + 0.01]; cur = cur[-1] if cur else beats[0]
    c.text((W - 24, PH - 36), credit_for(cur['photo']), sans(20), (240, 240, 236), 0.85, "ra")
    c.rect((0, PH, W, H), fill=PAPER); c.line([(80, PH + 2), (W - 80, PH + 2)], RULE, 3)
    t0 = cur['t']; a = prog(t, t0, 0.45) if beats.index(cur) > 0 else prog(t, 0, 0.3)
    y = PH + 90; col = COLORS[cur.get('color', 'ink')]
    if cur.get('kicker'): c.text((W / 2, y), cur['kicker'].upper(), sans(30, "SemiBold"), col, a, "ma"); y += 62
    s = cur.get('text', '')
    if s: y = wrapc(c, W / 2, y, s, bod(96 if len(s) < 24 else (80 if len(s) < 44 else 68), "700-normal"), INK, a)
    if cur.get('vis'): VIS[cur['vis']['type']](c, t, t0, y + 24, a, cur['vis'])
    c.text((W / 2, H - 92), "Follow for the next label we decode", sans(30, "Medium"), MUTED, 1, "ma")
    c.text((W / 2, H - 48), "Education, not medical advice · AI narration", sans(24), MUTED, 1, "ma")
    return c.im

def end_frame(t, dur, key='drop'):
    c = Canvas(W, H, (21, 25, 27))
    c.im.paste(ImageEnhance.Brightness(ph.cover(key, W, H, clamp(t / dur), (0.5, 0.45))).enhance(0.4), (0, 0)); c.redraw()
    a = prog(t, 0.1, 0.5)
    c.text((W / 2, 760), "The Formula Folio", bod(104), (242, 242, 238), a, "ma")
    wrapc(c, W / 2, 920, "We read the formula so you don’t overpay.", bod(56, "400-italic"), (230, 170, 98), a, 900)
    c.text((W / 2, 1120), "Follow for the next label", sans(38, "SemiBold"), (126, 200, 190), prog(t, 0.6), "ma")
    return c.im

# ---------- captions ----------
CAP_HDR = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Display,70,&H00ECF0EE,&H00ECF0EE,&H001B1915,&H001B1915,-1,0,0,0,100,100,0,0,3,18,0,2,60,60,790,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def word_cues(voice):
    """Caption chunks (<=~16 chars) from faster-whisper word timestamps."""
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    import numpy as np
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', voice, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'])
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    segs, _ = m.transcribe(audio, word_timestamps=True, language="en")
    words = [w for s in segs for w in s.words]
    cues = []; cur = [];
    for w in words:
        cur.append(w)
        txt = ''.join(x.word for x in cur).strip()
        if len(txt) >= 14 or txt[-1:] in ',.?!:':
            cues.append([cur[0].start, cur[-1].end, txt]); cur = []
    if cur: cues.append([cur[0].start, cur[-1].end, ''.join(x.word for x in cur).strip()])
    for i in range(len(cues) - 1):  # close small gaps
        if cues[i + 1][0] - cues[i][1] < 0.35: cues[i][1] = cues[i + 1][0]
    return cues

def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"

def render(spec, voice, starts, out, end_dur=2.6, cues=None):
    """spec: {header, beats:[{s: sentence_index | t: seconds, photo, focus, kicker, text, color, vis}]}"""
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', voice]).decode())
    beats = []
    for b in spec['beats']:
        b = dict(b); b['t'] = b['t'] if 't' in b else starts[b['s']]; beats.append(b)
    beats.sort(key=lambda b: b['t']); beats[0]['t'] = 0.0
    if cues is None: cues = word_cues(voice)
    work = out + '.work'; os.makedirs(work, exist_ok=True)
    with open(f'{work}/cap.ass', 'w') as f:
        f.write(CAP_HDR + ''.join(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{x}\n" for a, b, x in cues))
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", f"{work}/v.mp4"], stdin=subprocess.PIPE)
    for i in range(round(dur * FPS)): p.stdin.write(frame(i / FPS, spec['header'], beats, dur).tobytes())
    for i in range(round(end_dur * FPS)): p.stdin.write(end_frame(i / FPS, end_dur, spec.get('end_photo', 'drop')).tobytes())
    p.stdin.close(); assert p.wait() == 0
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'{work}/v.mp4', '-i', voice, '-filter_complex',
                    f"[1:a]apad=pad_dur={end_dur},loudnorm=I=-14:TP=-1.5:LRA=11[a];[0:v]ass={work}/cap.ass:fontsdir={FONTS}[v]",
                    '-map', '[v]', '-map', '[a]', '-t', str(dur + end_dur), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19',
                    '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', out + '.tmp.mp4'], check=True)
    os.replace(out + '.tmp.mp4', out)
    return out

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--spec', required=True); ap.add_argument('--voice', required=True)
    ap.add_argument('--starts', required=True, help='JSON list of sentence start times'); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    print(render(json.load(open(a.spec)), a.voice, json.load(open(a.starts)), a.out))
