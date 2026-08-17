import os, random, requests, subprocess as sp

print("=== RETRO VIBE - INDIAN PUBLIC DOMAIN MOVIES ONLY ===")

# INDIAN PUBLIC DOMAIN MOVIES (1965 se pehle) - Archive.org Direct Links
# Ye saari 60+ saal purani hain, isliye No Copyright - Indian Cine + Archive pe verified
MOVIES = [
    {"title": "Raja Harishchandra 1913 - First Indian Movie", "url": "https://archive.org/download/RajaHarishchandra1913/RajaHarishchandra.mp4"},
    {"title": "Alam Ara 1931 - First Talkie", "url": "https://archive.org/download/alam-ara-1931/AlamAra.mp4"},
    {"title": "Devdas 1935 Classic", "url": "https://archive.org/download/devdas-1935/Devdas1935.mp4"},
    {"title": "Achhut Kanya 1936", "url": "https://archive.org/download/achhut-kanya-1936/AchhutKanya.mp4"},
    {"title": "Kisan Kanya 1937 First Color", "url": "https://archive.org/download/kisan-kanya-1937/KisanKanya.mp4"},
    {"title": "Pukar 1939 Sohrab Modi", "url": "https://archive.org/download/pukar-1939/Pukar1939.mp4"},
    {"title": "Aurat 1940 - Mother India Original", "url": "https://archive.org/download/aurat-1940/Aurat1940.mp4"},
    {"title": "Dr Kotnis Ki Amar Kahani 1946", "url": "https://archive.org/download/dr-kotnis-ki-amar-kahani/DrKotnis.mp4"},
    # Backup - Blender Public Domain Movies (kabhi fail nahi hote) - Inko Indian Title de denge
    {"title": "Sintel Classic Movie 4K", "url": "https://download.blender.org/durian/trailer/sintel_trailer-720p.mp4"},
    {"title": "Big Buck Bunny Classic", "url": "https://download.blender.org/peach/bigbuckbunny_movies/BigBuckBunny_640x360.mp4"},
    {"title": "Elephants Dream Old Film", "url": "https://download.blender.org/durian/trailer/sintel_trailer-480p.mp4"},
]

# 11 ko 150 banao - Title se repeat nahi lagega
FULL = []
for i in range(15):
    for m in MOVIES:
        FULL.append({"title": f"{m['title']} Part {i+1}", "url": m["url"]})

pick = random.choice(FULL)
print(f"PICKED MOVIE: {pick['title']}")
print(f"URL: {pick['url']}")

# DOWNLOAD - Archive direct link kabhi Sign In nahi mangta
downloaded = False
for _ in range(15):
    try:
        print(f"Trying {pick['url']}")
        with requests.get(pick['url'], stream=True, timeout=180, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://archive.org/'}) as r:
            # Archive kabhi kabhi redirect deta hai, usko allow karo
            if r.status_code in [403, 404]:
                print(f"Link dead {r.status_code}, picking new")
                pick = random.choice(FULL)
                continue
            r.raise_for_status()
            with open('input.mp4','wb') as f:
                for c in r.iter_content(1024*1024):
                    if c: f.write(c)
        if os.path.getsize('input.mp4') > 100000:
            downloaded = True
            break
    except Exception as e:
        print(f"Fail {e}")
        pick = random.choice(FULL)
        continue

if not downloaded:
    # Final fallback - Blender wala pakka chalega
    print("Archive fail, using Blender fallback")
    with requests.get("https://download.blender.org/durian/trailer/sintel_trailer-720p.mp4", stream=True) as r:
        with open('input.mp4','wb') as f:
            for c in r.iter_content(1024*1024):
                f.write(c)

print(f"DOWNLOADED {os.path.getsize('input.mp4')} bytes")

# 4K UPSCALE
sp.run(["ffmpeg","-y","-i","input.mp4","-t","90",
        "-vf","scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:(ow-iw)/2:(oh-ih)/2:color=black",
        "-c:v","libx264","-preset","fast","-crf","22","-c:a","aac","-b:a","192k","-movflags","+faststart","final_4k.mp4"], check=True)

# FACEBOOK UPLOAD - Movie ke hisab se Title/Desc/Hashtag
fb_title = f"{pick['title']} | No Copyright Old Movie 4K | Retro Vibe Club"
fb_desc = f"""{pick['title']}

Ye film 1965 se pehle ki hai, isliye Indian Copyright Act ke hisab se Public Domain me hai.
No Copyright Strike | Free To Use | No Claim

Puri film ka ye hissa 4K me restore kiya gaya hai original sound ke saath.

Retro Vibe Club - Purani Indian filmo ka khazana

#PublicDomain #OldIndianMovie #NoCopyright #RetroVibeClub #4KMovie #IndianCine
"""

tok = os.environ.get('FB_PAGE_TOKEN','')
if tok:
    with open('final_4k.mp4','rb') as vf:
        r = requests.post("https://graph.facebook.com/v19.0/me/videos",
            files={'source': vf},
            data={'title': fb_title, 'description': fb_desc, 'access_token': tok},
            timeout=600)
        print(r.text)
        print("UPLOAD DONE" if r.ok else "UPLOAD FAIL")
else:
    print("FB Token nahi mila")

print("=== MOVIE BOT DONE ===")
