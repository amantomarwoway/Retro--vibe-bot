import os,random,requests,subprocess as sp,json,glob

SEARCH_POOL = [
 "ytsearch15:1940s hindi full movie public domain no copyright",
 "ytsearch15:1950s old hindi classic movie public domain",
 "ytsearch15:old hindi bhajan public domain no copyright full",
 "ytsearch15:bhojpuri lokgeet old folk public domain no copyright",
 "ytsearch15:nautanki nautanki old drama public domain",
 "ytsearch15:old hindi songs 1950s public domain free to use",
 "ytsearch15:ramleela old natak public domain",
 "ytsearch15:old devotional songs public domain"
]

query = random.choice(SEARCH_POOL)
print(f"SEARCHING: {query}")

os.system("rm -f f.mp4 c.mp4 t.jpg *.json *.part *.ytdl")

# Download random 1 from search - 480p fast
os.system(f'yt-dlp --no-warnings -q --no-playlist --write-info-json -f "best[height<=480][ext=mp4]/best[height<=480]/best" -o f.mp4 "{query}"')

if not os.path.exists("f.mp4") or os.path.getsize("f.mp4") < 1000000:
    print("YT fail, using Archive 100% safe backup")
    os.system("wget -q https://archive.org/download/Kismet1943/Kismet1943_512kb.mp4 -O f.mp4")
    raw_title = "Kismet 1943 Old Classic Hindi Film Public Domain No Copyright"
else:
    try:
        jf = glob.glob("*.json")[0]
        info = json.load(open(jf))
        raw_title = info.get('title','Old Classic Public Domain')
    except:
        raw_title = "Old Classic Hindi Film Public Domain 1950s"

raw_title = raw_title.replace("Full Movie","").replace("full movie","").strip()
print(f"TITLE RAW: {raw_title}")

# SEO GENERATOR
cat = "Old Film"
rl = raw_title.lower()
if "bhajan" in rl: cat="Bhajan"
elif "lokgeet" in rl or "folk" in rl: cat="Lokgeet"
elif "natak" in rl or "nautanki" in rl or "ramleela" in rl: cat="Natak"
elif "song" in rl: cat="Old Songs"

base = raw_title[:55]
TITLE = f"{base} | {cat} | Retro Vibe Club"[:65]

DESC = f"""{raw_title}

{cat} | 60+ Saal Purani | Public Domain | No Copyright | No Owner | Free To Use

Retro Vibe Club par aap dekh rahe hai purane zamane ki anmol yaadein. Ye video Public Domain me hai.

🎬 Category: {cat}
📅 Type: Old Classic / Folk Culture
🔓 License: Public Domain - No Copyright Strike

Rozana Old Film, Bhajan, Lokgeet, Natak dekhne ke liye Page ko Follow karein 🙏

#RetroVibeClub #{cat.replace(' ','')} #PublicDomain #NoCopyright #OldIsGold #OldHindiFilm #PuraneGane #LokSanskriti #VintageIndia #ClassicBollywood #FreeToUse #OldBhajan #BhojpuriLokgeet #Bundelkhandi #RajasthaniFolk #NoOwner

Keywords: {cat.lower()}, old hindi film, classic bollywood, public domain movies, no copyright, purani film, vintage india, retro vibe club
"""

TAGS = f"{cat}, Public Domain, No Copyright, Old Film, Retro Vibe Club, Old Is Gold, Vintage India, Free To Use"

print(f"FINAL TITLE: {TITLE}")

# CUT 90 SEC
sp.call(["ffmpeg","-y","-ss","90","-i","f.mp4","-t","90","-c:v","libx264","-preset","ultrafast","-b:v","700k","-c:a","aac","-b:a","96k","c.mp4"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
if not os.path.exists("c.mp4"): os.system("cp f.mp4 c.mp4")
sp.call(["ffmpeg","-y","-ss","2","-i","c.mp4","-vframes","1","t.jpg"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)

print(f"Ready {os.path.getsize('c.mp4')} bytes")

# UPLOAD
tok=os.environ['FB_PAGE_TOKEN']
vid=requests.post(f"https://graph.facebook.com/v19.0/me/videos", files={'source': open('c.mp4','rb')}, data={'title': TITLE, 'description': DESC, 'access_token': tok}, timeout=180).json()
print(vid)

if 'id' in vid and os.path.exists("t.jpg"):
    try:
        requests.post(f"https://graph.facebook.com/v19.0/{vid['id']}/thumbnails", files={'source': open('t.jpg','rb')}, data={'is_preferred':'true','access_token': tok}, timeout=30)
    except: pass
