# Task: approvals from chat (Marcus, Nov 26 2026)

Marcus works from his computer and does not want to approve things in Telegram. From now on he approves in his
chat with Claude, and Claude carries out his approvals on this server through a CLI.

1. Add a CLI (e.g. `python -m folio.approve`) with:
   - `list` — every pending/held/planned item with id, kind, slots (CT), status and flags, one line each.
   - `approve <id> [--note "..."]` — same effect as Marcus tapping Approve / Approve anyway on its card (record
     note "approved by Marcus in chat via Claude" + timestamp). Safety checks still run at post time as today.
   - `skip <id>` — same as tapping Skip.
   - `reschedule <id> <YYYY-MM-DD HH:MM>` (America/Chicago) — move all of an item's slots.
   - `replace <id> <file>` — swap the item's video file (keep slots, titles, captions, approval) and re-run checks;
     if a new flag appears, drop the approval and hold it.
   When any of these runs, edit the item's Telegram card to reflect it (no new card, no notification).
2. Telegram: stop sending a new card for each item. Keep one quiet daily digest only if something is held. Keep the
   existing bot running (Skip buttons still work), just no per-item cards unless an item is held for a safety reason.
3. Do now, on Marcus's instruction in chat: reschedule ff-p1-v4 (CeraVe 120h Short) to 2026-11-27 12:15 and
   approve it (posts YouTube + Instagram; TikTok is not connected yet).
4. Tests, commit, short report (include `list` output).
