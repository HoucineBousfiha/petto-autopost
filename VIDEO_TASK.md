# Weekly job: make 7 PETTO TikTok videos (one per day, Monday to Sunday)

You are running unattended. Do all steps without asking questions.

1. Read `BRAND.md` (and `brand/ASSETS.md` if it exists). Open `videos/example.html` to see how a video
   is built, and look at the last 14 entries of `videos/log.json` (if it exists) so ideas don't repeat.
2. Work out the dates of the next 7 days, starting tomorrow (`D1` … `D7`, format YYYY-MM-DD).
   Skip any date where `videos/<date>.mp4` already exists.
3. For each date, write `videos/<date>.html`: a **30-second, 1080×1920** motion design.
   - Root: `<div class="stage">` 1080×1920, links `../brand/brand.css`, only local files
     (brand fonts, `../brand/logo.png`, `../brand/assets/…`). No web fonts or remote images.
   - Animate with CSS `@keyframes` + `animation-delay` (see the example). Time is controlled by the renderer.
   - Structure: **hook in the first 2 seconds** (big headline), 3–5 scenes, last 3–4 seconds = end card
     (logo, PETTO wordmark, "Free on iOS & Android").
   - Keep every text on screen long enough to read (at least 2.5 s per line).
   - Safe zones: keep text out of the top 180px and bottom 400px (TikTok UI covers them) and 90px from the sides.
   - Big type: headlines 90–140px, body 40–50px. PETTO colours and fonts only. No emoji in the video.
   - Mix the week: 3 funny pet videos (pet texts, pet "reviews", "POV: your cat…", day vs day),
     2 useful tips (safe, general, "ask your vet" when relevant), 2 app feature demos (animated UI cards).
4. Render each one: `python render_video.py videos/<date>.html`
   (If playwright is missing: `pip install pillow playwright==1.56.0 --break-system-packages -q`. Never run `playwright install`.)
5. Check each video: extract frames at 1, 5, 10, 15, 20, 25 and 29 s with
   `ffmpeg -loglevel error -ss <t> -i videos/<date>.mp4 -frames:v 1 /tmp/<date>-<t>.png` and look at them.
   Fix and re-render anything cut off, overlapping, unreadable, or empty.
6. For each video write `videos/<date>.txt` with the TikTok caption: 1–2 short lines, a question or call
   to action, then 4–6 hashtags including `#PETTO` and `#pettok`.
7. Append one entry per video to `videos/log.json` (create it as `[]` if missing):
   `{"date": "<date>", "idea": "<one line>", "assets": [...]}`
8. Commit (`Weekly videos <D1> to <D7>`) and push to `main` (`git push origin HEAD:main`;
   if rejected, `git pull --rebase origin main` and push again).
9. Finish with a 7-line summary: date + idea for each video.
