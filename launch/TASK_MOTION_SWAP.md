# Task: swap in AI-motion versions (approved by Marcus in chat, Nov 26)

1. `cd /srv/folio/kit-repo && git pull`.
2. Check /srv/folio/logs/approvals.log: confirm the chat-approval CLI exists, and that ff-p1-v4 is at 2026-11-27 12:15 and approved. If not, finish TASK_CHAT_APPROVALS.md first.
3. Use the CLI `replace` for each item, swapping only the video file. Keep the same time, title, description, thumbnail, SRT and approval:
   - ff-v1 → launch/video1-final.mp4
   - ff-v1-s1 → launch/v1-short1-price-per-ml.mp4
   - ff-v1-s2 → launch/v1-short2-label-xray.mp4
   - ff-v1-s3 → launch/v1-short3-patent.mp4
   - ff-v2 → launch/video2-final.mp4
   - ff-v2-s1 → launch/v2-short1-up-to.mp4
   - ff-v2-s2 → launch/v2-short2-derm-tested.mp4
   - ff-v2-s3 → launch/v2-short3-8x.mp4
4. Check every file with ffprobe: duration > 0, there is an audio stream, and its sha256 matches the repo copy.
5. Do NOT send Telegram cards.
6. Write a summary to /srv/folio/logs/motion_swap.log. It should list each item with its id, scheduled time, approved flag and file sha256 (first 12 characters). Also copy the summary to /srv/folio/push-repo/status/motion_swap.txt, then commit and push it (push via github-ff).
