import os, json, random, requests, subprocess, pathlib, time, glob
import yt_dlp

PAGE_ID = os.getenv("FB_PAGE_ID")
TOKEN = os.getenv("FB_PAGE_TOKEN")
HISTORY_FILE = "posted_history.json"

QUERIES = [
    "Dharmendra Sholay scene 4K", "Dharmendra Dharam Veer fight",
    "Amrish Puri Mogambo Mr India dialogue", "Amrish Puri DDLJ scene",
    "Mithun Disco Dancer full song 4K", "Mithun Suraksha movie action",
    "Govinda Coolie No 1 comedy scene", "Govinda Hero No 1 song",
    "Achhut Kanya 1936 old movie", "Sant Tukaram vintage movie",
    "Old Bollywood black and white fight scene", "70s Bollywood 4K song"
] * 20

def clean():
    for f in glob.glob("input.*") + glob.glob("reel.*") + glob.glob("*.mp4") + glob.glob("*.webm"):
        try: os.remove(f)
        except: pass

def get_query():
    hist = []
    if pathlib.Path(HISTORY_FILE).exists():
        try: hist = json.loads(pathlib.Path(HISTORY_FILE).read_text())
        except: hist = []
    unused = [q for q in QUERIES if q not in hist]
    if not unused:
        hist = []
        unused = QUERIES
    q = random.choice(unused)
    hist.append(q)
    pathlib.Path(HISTORY_FILE).write_text(json.dumps(hist[-500:]))
    return q

def download_video(query):
    clean()
    print(f"Searching: {query}")
    ydl_opts = {
        'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
        'outtmpl': 'input.%(ext)s',
        'quiet': False,
        'noplaylist': True,
        'default_search': 'ytsearch1',
        'nocheckcertificate': True,
        'retries': 5,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(f"ytsearch1:{query}", download=True)

    # Find downloaded file
    files = glob.glob("input.*")
    if not files:
        raise Exception("YouTube download failed")

    src = files[0]
    print(f"Downloaded: {src}")

    # Convert to proper mp4 if needed
    if not src.endswith(".mp4"):
        subprocess.run(["ffmpeg","-y","-i",src,"-c:v","libx264","-c:a","aac","input.mp4"], check=True)
        os.remove(src)
        return "input.mp4"
    return src

def make_reel():
    start = random.randint(10, 60)
    cmd = ["ffmpeg","-y","-ss",str(start),"-i","input.mp4","-t","25",
           "-vf","crop=ih*9/16:ih,scale=1080:1920:flags=lanczos,eq=contrast=1.1:saturation=1.2",
           "-c:v","libx264","-crf","23","-preset","veryfast","-c:a","aac","-b:a","128k","reel.mp4"]
    subprocess.run(cmd, check=True)
    return "reel.mp4"

def upload(file, query):
    desc = f"{query} ✨ 4K Vintage | Retro Vibe\n.\n#RetroVibe #OldIsGold #FacebookReels"
    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/videos"
    with open(file, 'rb') as f:
        r = requests.post(url, data={'access_token': TOKEN, 'description': desc, 'published': 'true'}, files={'file': f}, timeout=600)
    print(f"FB Response: {r.text[:500]}")
    r.raise_for_status()

if __name__ == "__main__":
    clean()
    q = get_query()
    video = download_video(q)
    reel = make_reel()
    upload(reel, q)
    print("SUCCESS - Permanent YouTube Solution")
