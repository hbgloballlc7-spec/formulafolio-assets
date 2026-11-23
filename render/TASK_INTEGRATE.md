# Task: make the house-style renderer the only Short renderer (approved by Marcus, Nov 23 2026)

Marcus rejected the gold-on-black text/data style of the first two Shorts. The approved Formula Folio look is in
/srv/folio/kit (README.md there). Every Short from now on is rendered with /srv/folio/kit/lib/vshort.py from a spec.
The old note "finalize.py (approved design, do not restyle)" is obsolete: remove it.

Do all of this, working autonomously, then reply with a short report.

1. **Replace the two held Shorts.** New renders (house style) are at
   /srv/folio/work/shorts/FF_Short_p1_v2.mp4 and FF_Short_p2_v2.mp4 (same HeyGen narration, no new spend).
   - Move the old FF_Short_p1.mp4 / FF_Short_p2.mp4 to /srv/folio/work/shorts/rejected/ and put the v2 files in
     their place (same names), so nothing can ever post the old look.
   - Run the existing QA on both. The face check exists to block AI avatars/on-screen AI hosts. Real stock photos
     credited "Photo: Unsplash" are allowed, including portraits (photo keys deep1, deep2, asian, smile, young1,
     young2, young3, mirror, reader, docs, bath, micro). If the only QA flag is a face from those photos, it passes.
   - Supersede the two existing Telegram approval cards: edit or delete the old cards (or mark them superseded in
     state.db so their buttons do nothing) and send fresh approval cards for the new files, keeping the same slots
     (P1 CeraVe: Tue Nov 24 12:15 PM CT; P2 Bora Barrier: Wed Nov 25 12:15 PM CT), same titles/captions. Header line
     of each new card: "Rebuilt in the house style (real photography, brand name up top)."
2. **Scripted Shorts from now on** (`folio.scripted`): replace the finalize.py step with
   `python /srv/folio/kit/lib/vshort.py --spec <spec.json> --voice <narration> --starts <sentence_starts.json> --out <file>`.
   Specs live in /srv/folio/kit/specs/. P1 = p1_cerave_120h.json, P2 = p2_bora_barrier.json. For any new script,
   write a spec first (follow the kit README rules exactly: one beat per sentence or two, new photo each beat, never
   the same photo twice in a row, brand + product in the header, a data visual wherever the script has a number,
   prefer a Folio specimen card for the claim being decoded). If a spec can't be written, hold the Short and tell
   Marcus; never fall back to the old renderer. Keep a local specs folder at /srv/folio/specs/ for new specs (the
   kit folder is a git checkout that gets updated with `git -C /srv/folio/kit-repo pull`).
3. **Shorts cut from long videos** (`folio.pipeline` / `render.py`): same rule. Use the clip's audio as the voice,
   transcript sentence starts as --starts, and a spec written from the transcript. No captions-only or
   letterboxed 16:9 Shorts.
4. Keep every existing safety check, the AI-voice line, posting slots and caps unchanged.
5. Update app/README.md (Scripted Shorts section) to describe the new renderer, and run the test suite.
6. Report: what changed, the two new card message ids, and confirm the old cards can no longer post.
