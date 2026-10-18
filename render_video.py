"""Render an animated HTML design to a 1080x1920 MP4 (TikTok / Reels).
Usage: python render_video.py videos/2026-10-19.html [--seconds 30] [--fps 30]
Output: videos/<same-name>.mp4

How animation works: write normal CSS @keyframes / transitions (or Web Animations).
The renderer pauses every animation and steps time frame by frame, so the
output is smooth and identical every run. Optional: define window.seek = (t) => {...}
in the page for JS-driven motion (t = seconds).
If brand/audio/ contains .mp3/.m4a files, one is picked (by date) as background music.
"""
import argparse, datetime, shutil, subprocess, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
W, H = 1080, 1920


def ffmpeg_bin():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg not found: pip install imageio-ffmpeg --break-system-packages")


SEEK_JS = """(t) => {
  document.getAnimations().forEach(a => { a.pause(); a.currentTime = t * 1000; });
  if (typeof window.seek === 'function') window.seek(t);
}"""


def pick_audio():
    tracks = sorted(p for p in (ROOT / "brand" / "audio").glob("*") if p.suffix.lower() in (".mp3", ".m4a", ".wav"))
    if not tracks:
        return None
    return tracks[datetime.date.today().toordinal() % len(tracks)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--seconds", type=float, default=30)
    ap.add_argument("--fps", type=int, default=30)
    args = ap.parse_args()

    src = Path(args.html).resolve()
    out = src.with_suffix(".mp4")
    silent = src.with_name(src.stem + "_silent.mp4")
    frames = int(args.seconds * args.fps)
    ff = ffmpeg_bin()

    enc = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(args.fps),
                            "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium",
                            "-crf", "20", "-movflags", "+faststart", str(silent)], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        page.goto(src.as_uri())
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        for i in range(frames):
            page.evaluate(SEEK_JS, i / args.fps)
            enc.stdin.write(page.screenshot(type="jpeg", quality=92, clip={"x": 0, "y": 0, "width": W, "height": H}))
            if i % args.fps == 0:
                print(f"  {i // args.fps}s / {int(args.seconds)}s", flush=True)
        browser.close()
    enc.stdin.close()
    if enc.wait() != 0:
        sys.exit("ffmpeg encoding failed")

    audio = pick_audio()
    if audio:
        fade_at = max(args.seconds - 2, 0)
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(silent), "-i", str(audio),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                        "-af", f"afade=t=in:d=0.5,afade=t=out:st={fade_at}:d=2", "-shortest", str(out)], check=True)
        silent.unlink()
        print("music:", audio.name)
    else:
        silent.replace(out)
    print("rendered", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
