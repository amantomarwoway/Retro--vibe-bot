import os, random, requests, subprocess, re, time

PAGE_ID = os.getenv("FB_PAGE_ID")
TOKEN = os.getenv("FB_PAGE_TOKEN")

print(f"PAGE_ID: {PAGE_ID}")
print(f"TOKEN LENGTH: {len(TOKEN) if TOKEN else 0}")

def get_indian_cinema_video():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://indiancine.ma/"
    }
    # Step 1: Get film list from indiancine.ma
    list_url = "https://indiancine.ma/films?year_from=1930&year_to=1980"
    print(f"Fetching list: {list_url}")
    resp = requests.get(list_url, headers=headers, timeout=30)
    films = re.findall(r'href="/film/([a-zA-Z0-9-_]+)"', resp.text)
    films = list(set(films))
    
    if not films:
        raise Exception("Indian Cine.ma se films nahi mili")
    
    random.shuffle(films)
    
    for film_slug in films[:10]: # 10 films try karega
        film_url = f"https://indiancine.ma/film/{film_slug}"
        print(f"Checking: {film_url}")
        try:
            f_resp = requests.get(film_url, headers=headers, timeout=30)
            # mp4 direct link
            mp4 = re.search(r'"(https?://[^"]+\.mp4[^"]*)"', f_resp.text)
            if mp4:
                print(f"FOUND MP4: {mp4.group(1)[:100]}")
                return mp4.group(1), film_slug
            
            m3u8 = re.search(r'"(https?://[^"]+\.m3u8[^"]*)"', f_resp.text)
            if m3u8:
                print(f"FOUND M3U8: {m3u8.group(1)[:100]}")
                return m3u8.group(1), film_slug
        except Exception as e:
            print(f"Skip {film_slug}: {e}")
            continue
        time.sleep(2)
    
    raise Exception("Kisi bhi film me video link nahi mila")

def make_4k_reel(video_url):
    output = "reel_4k.mp4"
    # ffmpeg se 30 sec ka vertical 4K reel (2160x3840)
    cmd = [
        "ffmpeg", "-y",
        "-headers", "Referer: https://indiancine.ma/\r\nUser-Agent: Mozilla/5.0\r\n",
        "-i", video_url,
        "-ss", "90", "-t", "28",
        "-vf", "crop=ih*9/16:ih,scale=2160:3840:flags=lanczos",
        "-c:v", "libx264", "-crf", "19", "-preset", "fast",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        output
    ]
    print("Running FFmpeg for 4K Reel...")
    subprocess.run(cmd, check=True)
    return output

def upload_as_reel(file_path, film_name):
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/video_reels"
    title = f"{film_name.replace('-',' ').title()} | Rare 4K Clip ✨\n\nFrom Indian Cine.ma Archive - Non Copyrighted\n\n#RetroVibe #IndianCineMa #RetroIndia #4KReels #OldIsGold #ClassicCinema #FacebookReels #ViralReels #DesiReels #Nostalgia"
    
    with open(file_path, 'rb') as f:
        files = {'video_file': f}
        data = {
            'access_token': TOKEN,
            'description': title,
            'published': 'true'
        }
        # Graph API reels upload
        r = requests.post(url, files={'file': f}, data=data, timeout=400)
    
    # dusra method try agar pehla fail
    if r.status_code != 200 or "id" not in r.text:
        print(f"First method failed: {r.text}")
        # Reels ke liye /videos endpoint
        url2 = f"https://graph.facebook.com/v19.0/{PAGE_ID}/videos"
        with open(file_path, 'rb') as f:
            r = requests.post(url2, files={'file': f}, data=data, timeout=400)
    
    print(f"FINAL RESPONSE: {r.text}")
    if r.status_code != 200:
        raise Exception(f"UPLOAD FAIL: {r.text}")
    print("UPLOAD SUCCESS - REEL POSTED")

if __name__ == "__main__":
    v_url, name = get_indian_cinema_video()
    reel_file = make_4k_reel(v_url)
    upload_as_reel(reel_file, name)
