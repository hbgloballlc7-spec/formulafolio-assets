# Task: load the Formula Folio launch (approved by Marcus in chat, Nov 25 2026)

Marcus approved this exact batch: two long videos and six Shorts in /srv/folio/kit-repo/launch/, described in
manifest.json (files, titles, descriptions/captions, thumbnails, YouTube caption files, publish times in
America/Chicago, platforms). Load it into the existing scheduler, working autonomously, then report.

1. Register every manifest item as a pre-made item. Use the manifest's titles, descriptions, captions, hashtags and
   publish_at times exactly. Do NOT cut or render any new Shorts from the two long videos: the six Shorts here
   are the Shorts for these videos. Do not re-render or re-encode the files.
2. Record Marcus's approval (Nov 25, in chat) on every item so they post at their times without a tap. Still run
   every safety check. If an item hits any check, hold it and send a tap-only card that says why; don't post it.
   Send one Telegram summary card listing every item and its time, with a Skip button per item (Skip must still
   work right up to publish time).
3. Long videos: YouTube only, made_for_kids false, altered/synthetic flag on, AI-voice line present (it is in the
   descriptions). Set the custom thumbnail and upload the .srt captions if Upload-Post (or another tool already
   on this server) supports it; if not, say so in the report and don't build a workaround.
4. Shorts: YouTube Shorts, Instagram Reels, and TikTok if the formulafolio Upload-Post profile has TikTok
   connected at post time (check right before each post; if not connected, post to the others and note it).
5. Make sure nothing else is scheduled into these slots and that the daily caps still allow them.
6. Commit any code changes. Report: each item with its scheduled time and platforms, the summary card's message
   id, any holds, and whether thumbnails and captions were set.
