# Formula Folio Short renderer (house style)

Every Formula Folio Short must use this renderer. Look: full-bleed real photography (Unsplash, free commercial
license) with slow Ken Burns on top, the product/brand name large in the header, one big serif statement per beat
in a paper panel, a data visual where there's a number, burned captions (Inter Display), branded end card.
No gold-on-black, no text-only slides, no plain backgrounds.

    python lib/vshort.py --spec specs/<name>.json --voice <narration.m4a> --starts <sentence_starts.json> --out out.mp4

Spec: {"header": "<Brand Product>", "end_photo": key, "beats": [{"s": <sentence index>, "photo": <key in photos/>,
"focus": [x,y], "kicker": "small caps line", "text": "big statement (<44 chars)", "color": ink|teal|amber|ox,
"vis": {"type": bars|chips|stamp|rank|stat, ...}}]}  — one beat per sentence or two; change the photo every beat;
never the same photo twice in a row. Photo keys: see photos/INDEX.md. spec_* = Folio specimen cards (make new ones
for new claims), ai_* = AI bottles with Folio labels. Requires: Pillow, numpy, faster-whisper, ffmpeg with libass.
