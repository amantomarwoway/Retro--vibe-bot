import os, json, random, requests, subprocess, pathlib, time

PAGE_ID = os.getenv("FB_PAGE_ID")
TOKEN = os.getenv("FB_PAGE_TOKEN")
HISTORY_FILE = "posted_history.json"

# FIXED LINKS - %20 lagaya hai, space hataya
FREE_FILMS = [
    "https://archive.org/download/AchhutKanya1936/AchhutKanya%20512kb.mp4",
    "https://archive.org/download/SitaSwayamvar1936/SitaSwayamvar%201936%20512kb.mp4",
    "https://archive.org/download/SantTukaram1936/SantTukaram1936%20512kb.mp4",
    "https://archive.org/download/DrKotnisKiAmarKahani/DrKotnisKiAmarKahani%20512kb.mp4",
    "https://archive.org/download/DhoopChhaon1935/DhoopChhaon%20512kb.mp4",
    "https://archive.org/download/JamaiBabu1931/JamaiBabu%20512kb.mp4",
    "https://archive.org/download/Phulwari1939/Phulwari%20512kb.mp4",
    "https://archive.org/download/AchhutKanya1936/AchhutKanya%20512kb.mp4",
]

def get_unused_film():
    history = []
    if pathlib.Path(HISTORY_FILE).exists():
        try:
            history = json.loads(pathlib.Path(HISTORY_FILE).read_text())
        except:
            history = []
    
    unused = [f for f in FREE_FILMS if f not in history]
    if not unused:
        unused = FREE_FILMS
        history = []
    
    film = random.choice(unused)
    history.append(film)
    pathlib.Path(HISTORY_FILE).write_text(json.dumps(history[-200:]))
    return film

def make_reel(url):
    out = "reel.mp4"
    url = url.replace(" ", "%20")
    print(f"Downloading: {url}")

    # Download first - FFmpeg direct URL se fail hota hai
    try:
        with requests.get(url, stream=True, timeout=120) as r:
            r.raise_for_status()
            with open("input.mp4", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception as e:
        print(f"Download fail: {e}, trying next...")
        raise e

    print("Download done, making 9:16 reel...")
    start = random.randint(60, 180)
    
    cmd = [
        "ffmpeg","-y",
        "-ss", str(start),
        "-i", "input.mp4",
        "-t", "25",
        "-vf", "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos,eq=contrast=1.1:saturation=1.2",
        "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "128k",
        out
    ]
    subprocess.run(cmd, check=True)
    print("Reel ready")
    return out

def upload(file, source_url):
    name = source_url.split("/")[-2][:50]
    desc = f"{name} | Rare 4K Vintage Clip ✨ Retro Vibe\n\n#RetroVibe #IndianCineMa #OldIsGold #FacebookReels #VintageIndia #4K"
    
    upload_url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/videos"
    with open(file, 'rb') as f:
        r = requests.post(upload_url, data={
            'access_token': TOKEN,
            'description': desc,
            'published': 'true'
        }, files={'file': f}, timeout=400)
    print(f"UPLOAD RESPONSE: {r.text}")
    if r.status_code != 200:
        raise Exception(f"Upload fail: {r.text}")

if __name__ == "__main__":
    print(f"TOKEN LENGTH: {len(TOKEN) if TOKEN else 0}")
    for attempt in range(3): # 3 baar try karega agar link fail ho
        try:
            film_url = get_unused_film()
            reel = make_reel(film_url)
            upload(reel, film_url)
            print("SUCCESS!")
            break
        except Exception as e:
            print(f"Attempt {attempt+1} fail: {e}")
            time.sleep(5)
            if attempt == 2:
                raise e
