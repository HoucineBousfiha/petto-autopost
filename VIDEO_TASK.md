# Weekly job: make 7 PETTO TikTok videos (one per day, Monday to Sunday)

You are running unattended. Do all steps without asking questions.

1. Read `BRAND.md` (and `brand/ASSETS.md` if it exists; if `brand/assets/` has files not listed there, look
   at them and add them). Open `videos/example.html` and `videos/example.voice.json` to see how a video and
   its narration are built. Look at the last 14 entries of `videos/log.json` (if it exists) so ideas don't repeat.
2. Work out the dates of the next 7 days, starting tomorrow (`D1` … `D7`, format YYYY-MM-DD).
   Skip any date where `videos/<date>.silent.mp4` already exists.
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
4. For each date, write `videos/<date>.voice.json`: the voice-over and sound effects (same format as the example).
   - Narrator: a warm, friendly, slightly playful friend explaining. Short spoken sentences, contractions,
     no hashtags, no emoji, write numbers and times as words ("six thirty").
   - Each `"text"` cue starts when its scene appears (use the scene's animation-delay as `"t"`).
   - Budget: about **2.5 spoken words per second**. A cue must fit before the next cue starts.
     Total narration 55–70 words, ending with "PETTO. Free on iOS and Android." on the end card.
   - Sound effects: `"pop"` when a card/bubble pops in, `"whoosh"` on scene changes, `"ding"` for a
     success moment, `"tap"` for UI taps. Don't overdo it (max ~12 per video).
   - Voice: use `"af_heart"` by default; for variety you may use `"af_bella"` or `"am_michael"`.
5. Render each one: `python render_video.py videos/<date>.html` → writes `videos/<date>.silent.mp4`.
   (If playwright is missing: `pip install pillow playwright==1.56.0 --break-system-packages -q`. Never run `playwright install`.)
   Do NOT create `videos/<date>.mp4` yourself: after you push, a GitHub Action adds the voice, music and
   sound effects and saves the final `videos/<date>.mp4`.
6. Check each video: extract frames at 1, 5, 10, 15, 20, 25 and 29 s with
   `ffmpeg -loglevel error -ss <t> -i videos/<date>.silent.mp4 -frames:v 1 /tmp/<date>-<t>.png` and look at them.
   Fix and re-render anything cut off, overlapping, unreadable, or empty. Check the narration matches what is on screen.
7. For each video write `videos/<date>.txt` with the TikTok caption: 1–2 short lines, a question or call
   to action, then 4–6 hashtags including `#PETTO` and `#pettok`.
8. Append one entry per video to `videos/log.json` (create it as `[]` if missing):
   `{"date": "<date>", "idea": "<one line>", "voice": "<voice>", "assets": [...]}`
9. Commit (`Weekly videos <D1> to <D7>`) and push to `main` (`git push origin HEAD:main`;
   if rejected, `git pull --rebase origin main` and push again).
10. Finish with a 7-line summary: date + idea for each video.
