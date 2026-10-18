# Daily job: design 4 PETTO posts and queue them

You are running unattended. Do all steps without asking questions.

1. Read `BRAND.md`. Open and look at `posts/fun1-forgot-list.png`, `posts/fun2-dog-could-text.png`,
   `posts/fun3-honest-cat-review.png` and `posts/fun4-your-day-vs-theirs.png`: they are real PETTO
   posts, so match their style, colours, layout quality and humour. Look at the last ~12 entries of
   `queue.json` so today's ideas don't repeat recent topics or formats.
   Read `brand/ASSETS.md`. If `brand/assets/` has files not listed in `brand/ASSETS.md`, look at them
   and add them to the table.
2. Use today's date as `D` (YYYY-MM-DD). If `designs/D-1.html` already exists, today's posts were already made: stop.
3. Write 4 designs following the daily mix in `BRAND.md`: `designs/D-1.html` … `designs/D-4.html`.
   Each is a full HTML page that links `../brand/brand.css`, has `<div class="post">` as its root (1080×1350),
   and uses only local files (no web fonts, no remote images). Keep all text and the logo at least
   100px from the left and right edges.
4. Render. First run `python -c "import playwright"`. Only if that fails, install with exactly:
   `pip install pillow playwright==1.56.0 --break-system-packages -q`
   Never run `playwright install`. Then run
   `python render.py designs/D-1.html designs/D-2.html designs/D-3.html designs/D-4.html`.
   This writes `posts/D-1.jpg` … `posts/D-4.jpg`.
5. Look at every JPEG (open the image). Fix and re-render any design with overflowing or cut-off text,
   overlapping elements, low contrast or empty areas.
6. Append 4 entries to the end of `queue.json`, in order 1→4:
   `{"image": "D-1.jpg", "caption": "...", "assets": ["file1.png", ...], "posted_at": null}`
   `assets` lists the `brand/assets/` file names the design uses (`[]` for text-only), so rotation can be tracked.
   Keep it valid JSON and don't change existing entries.
7. Commit (`Daily posts D`) and push to the `main` branch (`git push origin HEAD:main`).
   If the push is rejected, run `git pull --rebase origin main` and push again.
8. Finish with a 2-line summary: the 4 post ideas, and how many unposted items are now in the queue.
