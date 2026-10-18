"""
PETTO Instagram autoposter.
Each run publishes the NEXT unposted item from queue.json to Instagram,
then marks it as posted. GitHub Actions runs this 4x per day.

Needs env vars (GitHub secrets): IG_USER_ID, IG_ACCESS_TOKEN
"""
import json, os, subprocess, sys, time, datetime, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image

API_VERSION = os.environ.get("IG_API_VERSION", "v25.0")
API = f"https://graph.instagram.com/{API_VERSION}"
ROOT = Path(__file__).parent
QUEUE = ROOT / "queue.json"
REPO = os.environ["GITHUB_REPOSITORY"]          # e.g. yourname/petto-autopost
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
IG_USER_ID = os.environ["IG_USER_ID"]
TOKEN = os.environ["IG_ACCESS_TOKEN"]


def call(method, path, **params):
    params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    if method == "GET":
        req = urllib.request.Request(f"{url}?{data.decode()}")
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Instagram API error {e.code}: {e.read().decode()}")


def git(*args):
    subprocess.run(["git", *args], check=True)


def prepare_jpeg(src: Path) -> Path:
    """Instagram API only accepts JPEG, feed ratio 4:5 (0.8) to 1.91:1.
    Converts PNG -> JPEG and pads too-tall images (3:4, 9:16) to 4:5."""
    img = Image.open(src).convert("RGB")
    w, h = img.size
    if w / h < 0.8:                      # too tall for a feed post
        new_w = round(h * 0.8)
        bg = img.getpixel((0, 0))        # pad with the design's background colour
        canvas = Image.new("RGB", (new_w, h), bg)
        canvas.paste(img, ((new_w - w) // 2, 0))
        img = canvas
    if img.width > 1440:                 # keep files light
        img = img.resize((1080, round(img.height * 1080 / img.width)), Image.LANCZOS)
    out = src.with_name(src.stem + "_ig.jpg")
    img.save(out, "JPEG", quality=92)
    return out


def main():
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    item = next((p for p in queue if not p.get("posted_at")), None)
    if item is None:
        print("Queue is empty - nothing to post. Add new posts to queue.json.")
        return

    src = ROOT / "posts" / item["image"]
    if not src.exists():
        sys.exit(f"Image not found: posts/{item['image']}")

    jpg = prepare_jpeg(src)
    rel = jpg.relative_to(ROOT).as_posix()
    # Push the JPEG so Instagram can download it from a public URL
    git("add", rel)
    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 0:
        git("commit", "-m", f"Prepare {rel}")
        git("push")
        time.sleep(20)                   # give GitHub a moment to serve the file
    image_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{urllib.parse.quote(rel)}"
    print("Image URL:", image_url)

    # 1) create media container
    container = call("POST", f"{IG_USER_ID}/media",
                     image_url=image_url, caption=item["caption"])["id"]
    # 2) wait until Instagram has processed it
    for _ in range(10):
        status = call("GET", container, fields="status_code").get("status_code")
        print("Container status:", status)
        if status == "FINISHED":
            break
        if status in ("ERROR", "EXPIRED"):
            sys.exit(f"Container failed with status {status}")
        time.sleep(30)
    # 3) publish
    media_id = call("POST", f"{IG_USER_ID}/media_publish", creation_id=container)["id"]
    print("Published! media id:", media_id)

    item["posted_at"] = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    item["media_id"] = media_id
    QUEUE.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    git("add", "queue.json")
    git("commit", "-m", f"Posted {item['image']}")
    git("push")


if __name__ == "__main__":
    main()
