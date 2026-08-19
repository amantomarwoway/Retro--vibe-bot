import os, json, random, requests, subprocess, pathlib

PAGE_ID = os.getenv("FB_PAGE_ID")
TOKEN = os.getenv("FB_PAGE_TOKEN")
HISTORY_FILE = "posted_history.json"

# 100% FREE - Archive.org public domain (No Copyright)
FREE_FILMS = [
    # Dharmendra Early (Ab Public Domain)
    "https://archive.org/download/PhoolAurPatthar1966/PhoolAurPatthar_512kb.mp4",
    "https://archive.org/download/Anupama1966/Anupama_512kb.mp4",
    "https://archive.org/download/AayeDinBaharKe/AayeDinBaharKe_512kb.mp4",
    # Purani Classics
    "https://archive.org/download/SitaSwayamvar1936/SitaSwayamvar_512kb.mp4",
    "https://archive.org/download/SantTukaram1936/SantTukaram_512kb.mp4",
    "https://archive.org/download/AchhutKanya1936/AchhutKanya_512kb.mp4",
    "https://archive.org/download/DrKotnisKiAmarKahani/DrKotnis_512kb.mp4",
    "https://archive.org/download/JamaiBabu1931/JamaiBabu_512kb.mp4",
    "https://archive.org/download/DhoopChhaon1935/DhoopChhaon_512kb.mp4",
    # Aur 150+ links add kar sakta hai isi list me...
]

# History load - Repeat rokne ke liye
def get_unused_film():
    history = []
    if pathlib.Path(HISTORY_FILE).exists():
        history = json.loads(pathlib.Path(HISTORY_FILE).read_text())
    
    unused = [f for f in FREE_FILMS if f not in history]
    if not unused: # sab ho gaye to reset
        unused = FREE_FILMS
        history = []
    
    film = random.choice(unused)
    history.append(film)
    pathlib.Path(HISTORY_FILE).write_text(json.dumps(history[-500:])) # last 500 yaad rakhega
    return film

def make_reel(url):
    out = "reel.mp4"
    # Random 20-30 sec ka part, vertical 9:16 me
    start = random.randint(60, 300)
    cmd = ["ffmpeg","-y","-ss",str(start),"-i",url,"-t","25",
           "-vf","crop=ih*9/16:ih,scale=1080:1920:flags=lanczos,eq=contrast=1.1:saturation=1.2",
           "-c:v","libx264","-crf","22","-preset","fast","-c:a","aac","-b:a","128k", out]
    subprocess.run(cmd, check=True)
    return out

def upload(file, source_url):
    name = source_url.split("/")[-2].replace("1966","").replace("_"," ")
    desc = f"{name} | Rare Clip 4K ✨\n\nDharmendra | Govinda | Mithun | Amrish Puri ke daur ki yaadein. Old is Gold! 🎬\n\n#RetroVibe #IndianCineMa #OldIsGold #Dharmendra #Govinda #Mithun #AmrishPuri #FacebookReels #VintageIndia"
    
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/videos"
    with open(file, 'rb') as f:
        r = requests.post(url, data={'access_token': TOKEN, 'description': desc, 'published': 'true'}, files={'file': f}, timeout=400)
    print(r.text)

if __name__ == "__main__":
    film_url = get_unused_film()
    print(f"Selected: {film_url}")
    reel = make_reel(film_url)
    upload(reel, film_url)
