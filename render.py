"""Render design HTML files to 1080x1350 JPEGs for Instagram.
Usage: python render.py designs/2026-10-19-1.html [more.html ...]
Output: posts/<same-name>.jpg
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).parent


def main(files):
    (ROOT / "posts").mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for f in files:
            src = Path(f).resolve()
            page.goto(src.as_uri())
            page.wait_for_load_state("networkidle")
            page.evaluate("document.fonts.ready")
            png = ROOT / "posts" / (src.stem + ".png")
            page.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
            jpg = png.with_suffix(".jpg")
            Image.open(png).convert("RGB").save(jpg, "JPEG", quality=92)
            png.unlink()
            print("rendered", jpg.relative_to(ROOT))
        browser.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
