# Daily job: design 4 PETTO posts and queue them

You are running unattended. Do all steps without asking questions.

1. Read `BRAND.md` and look at the last ~12 entries of `queue.json` so today's ideas don't repeat recent topics or formats.
2. Use today's date as `D` (YYYY-MM-DD). If `designs/D-1.html` already exists, today's posts were already made: stop.
3. Write 4 designs following the daily mix in `BRAND.md`: `designs/D-1.html` … `designs/D-4.html`.
   Each is a full HTML page that links `../brand/brand.css`, has `<div class="post">` as its root (1080×1350),
   and uses only local files (no web fonts, no remote images).
4. Render: `pip install pillow playwright --break-system-packages -q` (if needed), then
   `python render.py designs/D-1.html designs/D-2.html designs/D-3.html designs/D-4.html`.
   This writes `posts/D-1.jpg` … `posts/D-4.jpg`.
5. Look at every JPEG (open the image). Fix and re-render any design with overflowing or cut-off text,
   overlapping elements, low contrast or empty areas.
6. Append 4 entries to the end of `queue.json`, in order 1→4:
   `{"image": "D-1.jpg", "caption": "...", "posted_at": null}`
   Keep it valid JSON and don't change existing entries.
7. Commit (`Daily posts D`) and push to the default branch.
8. Finish with a 2-line summary: the 4 post ideas, and how many unposted items are now in the queue.
