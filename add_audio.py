"""Add a friendly voice-over, background music and sound effects to PETTO videos.
Runs in GitHub Actions (it needs internet once to download the free Kokoro voice model).

For every videos/<D>.voice.json that has a videos/<D>.silent.mp4 but no videos/<D>.mp4 yet:
  1. speaks each narration cue with Kokoro TTS at its start time
  2. adds sound effects (pop / whoosh / ding / tap) at their times
  3. adds a background track from brand/audio/ (if any), auto-lowered under the voice
  4. writes videos/<D>.mp4 (final video for TikTok)

voice.json format:
{
  "voice": "af_heart",            optional, Kokoro voice name
  "speed": 1.0,                   optional
  "music_volume": 0.30,           optional (0-1)
  "cues": [ {"t": 0.4, "text": "Ever wondered what your dog would text you?"},
            {"t": 5.5, "sfx": "whoosh"},
            {"t": 7.0, "sfx": "pop"} ]
}
To redo a video's sound, delete videos/<D>.mp4 and push.
"""
import datetime, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT = Path(__file__).parent
SR = 24000
MODEL_DIR = Path(os.environ.get("KOKORO_DIR", ROOT / ".kokoro"))
FF = shutil.which("ffmpeg") or sys.exit("ffmpeg not found")

_tts = None


def tts(text, voice, speed):
    global _tts
    if os.environ.get("MOCK_TTS"):                       # offline test mode
        n = int(SR * 0.075 * len(text.split()) / speed * 4)
        return (0.2 * np.sin(np.linspace(0, 2 * np.pi * 220 * n / SR, n))).astype(np.float32)
    if _tts is None:
        from kokoro_onnx import Kokoro
        _tts = Kokoro(str(MODEL_DIR / "kokoro-v1.0.onnx"), str(MODEL_DIR / "voices-v1.0.bin"))
    samples, sr = _tts.create(text, voice=voice, speed=speed, lang="en-us")
    if sr != SR:
        sys.exit(f"unexpected sample rate {sr}")
    return samples.astype(np.float32)


def sfx(kind):
    t = lambda d: np.linspace(0, d, int(SR * d), endpoint=False)
    rng = np.random.default_rng(7)
    if kind == "pop":
        x = t(0.09); f = 900 - 5000 * x
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 45)
    elif kind == "tap":
        x = t(0.05); s = np.sin(2 * np.pi * 1600 * x) * np.exp(-x * 90)
    elif kind == "ding":
        x = t(0.9); s = sum(a * np.sin(2 * np.pi * f * x) for f, a in ((1320, 1), (2640, .35), (3960, .15))) * np.exp(-x * 5)
    elif kind == "whoosh":
        x = t(0.45); n = rng.standard_normal(len(x))
        n = np.convolve(n, np.ones(12) / 12, mode="same")          # soften
        s = n * np.sin(np.pi * x / 0.45) ** 2
    else:
        print("  unknown sfx:", kind); return np.zeros(1, np.float32)
    s = s / (np.abs(s).max() + 1e-9) * 0.35
    return s.astype(np.float32)


def place(track, clip, start):
    i = int(start * SR)
    if i >= len(track):
        return
    j = min(len(track), i + len(clip))
    track[i:j] += clip[: j - i]


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 30)


def pick_music(day):
    tracks = sorted(p for p in (ROOT / "brand" / "audio").glob("*") if p.suffix.lower() in (".mp3", ".m4a", ".wav"))
    if not tracks:
        return None
    try:
        n = datetime.date.fromisoformat(day).toordinal()
    except ValueError:
        n = len(day)
    return tracks[n % len(tracks)]


def process(spec_path):
    day = spec_path.name.split(".")[0]
    silent = spec_path.with_name(f"{day}.silent.mp4")
    final = spec_path.with_name(f"{day}.mp4")
    if not silent.exists() or final.exists():
        return False
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    voice, speed = spec.get("voice", "af_heart"), float(spec.get("speed", 1.0))
    total = duration(silent)
    vtrack = np.zeros(int(SR * total) + SR, np.float32)
    ftrack = np.zeros_like(vtrack)
    lines = sorted((c for c in spec["cues"] if c.get("text")), key=lambda c: c["t"])
    cursor = 0.0
    for k, c in enumerate(lines):
        start = max(float(c["t"]), cursor)
        nxt = lines[k + 1]["t"] if k + 1 < len(lines) else total - 0.3
        clip = tts(c["text"], voice, speed)
        room = nxt - start - 0.15
        if len(clip) / SR > room > 0.5:                          # too long: speak a bit faster (max 1.3x)
            clip = tts(c["text"], voice, min(1.3, speed * len(clip) / SR / room))
        place(vtrack, clip, start)
        cursor = start + len(clip) / SR + 0.15
        if cursor > nxt + 0.05:
            print(f"  note: line at {c['t']}s runs {cursor - nxt:.1f}s into the next one")
    for c in spec["cues"]:
        if c.get("sfx"):
            place(ftrack, sfx(c["sfx"]), float(c["t"]))

    with tempfile.TemporaryDirectory() as tmp:
        vwav, fwav = Path(tmp, "v.wav"), Path(tmp, "f.wav")
        sf.write(vwav, np.clip(vtrack, -1, 1), SR)
        sf.write(fwav, np.clip(ftrack, -1, 1), SR)
        music = pick_music(day)
        mv = float(spec.get("music_volume", 0.30))
        fade = max(total - 2, 0)
        if music:
            inputs = ["-i", str(silent), "-i", str(vwav), "-i", str(fwav), "-stream_loop", "-1", "-i", str(music)]
            graph = (f"[3:a]atrim=0:{total},volume={mv},afade=t=in:d=1,afade=t=out:st={fade}:d=2,aresample={SR}[m];"
                     f"[1:a]volume=1.6,asplit=2[v1][v2];"
                     f"[m][v1]sidechaincompress=threshold=0.03:ratio=6:attack=30:release=500[md];"
                     f"[md][v2][2:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95[a]")
        else:
            inputs = ["-i", str(silent), "-i", str(vwav), "-i", str(fwav)]
            graph = f"[1:a]volume=1.6[v];[v][2:a]amix=inputs=2:duration=first:normalize=0,atrim=0:{total},alimiter=limit=0.95[a]"
        subprocess.run([FF, "-y", "-loglevel", "error", *inputs, "-filter_complex", graph,
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", "-movflags", "+faststart", str(final)], check=True)
    print(f"made {final.relative_to(ROOT)}  (voice {voice}, music: {music.name if music else 'none'})")
    return True


def main():
    specs = sorted((ROOT / "videos").glob("*.voice.json"))
    done = sum(process(p) for p in specs)
    print(f"{done} video(s) finished")


if __name__ == "__main__":
    main()
