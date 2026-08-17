import os,random,requests,subprocess as sp,time,json,glob

# ===== 100+ POOL PER CATEGORY =====
# Old Film ke 30 IDs x 4 = 120, baaki audio ke liye YT search best hai
ARCHIVE_FILMS = [
"Kismet1943","Mahal1949","Barsaat1949","Awaara1951","Aan1952","Anarkali1953","Shree4201955","CID1956",
"MotherIndia1957","Madhumati1958","Anari1959","Mughal-e-Azam1960","Junglee1961","BeesSaalBaad1962",
"Sangam1964","Dosti1964","GungaJumna1961","Milan1967","Upkar1967","RamAurShyam1967","Pakeezah1971",
"Sholay1975","Deewaar1975","AmarAkbarAnthony1977","Don1978","MuqaddarKaSikandar1978"
] * 5 # 130 ho gaye

YT_SEARCH = {
 "Old Film": ["ytsearch20:1940s hindi movie public domain","ytsearch20:1950s old bollywood full movie no copyright","ytsearch20:1960s classic hindi film public domain"],
 "Bhajan": ["ytsearch20:old krishna bhajan public domain no copyright","ytsearch20:shiv bhajan old 1950s no copyright","ytsearch20:ram bhajan old public domain","ytsearch20:hanuman bhajan old no copyright"],
 "Lokgeet": ["ytsearch20:bhojpuri lokgeet old folk public domain","ytsearch20:rajasthani lokgeet old public domain","ytsearch20:haryanvi lokgeet old no copyright","ytsearch20:bundelkhandi lokgeet public domain"],
 "Natak": ["ytsearch20:nautanki natak old public domain","ytsearch20:ramleela full natak old public domain","ytsearch20:bhavai natak old folk drama"],
 "Old Songs": ["ytsearch20:old hindi songs 1940s public domain","ytsearch20:1950s hindi geet public domain no copyright"]
}

cat = random.choice(["Old Film","Old Film","Old Film","Bhajan","Lokgeet","Natak","Old Songs"])
print(f"TODAY CATEGORY: {cat}")

os.system("rm -f f.mp4 c.mp4 t.jpg *.json *.part")

raw_title = ""
downloaded = False

# ===== TRY 1: YOUTUBE (with bot bypass) =====
if cat!= "Old Film" or random.random() > 0.5: # Old Film me 50% YT try karega
    try:
        q = random.choice(YT_SEARCH[cat])
        print(f"TRYING YT: {q}")
        # Bot bypass trick: android client
        cmd = f'yt-dlp --no-warnings -q --no-playlist --write-info-json --extractor-args "youtube:player_client=android" -f "best[height<=480][ext=mp4]/best[height<=480]/b" -o f.mp4 "{q}" --max-downloads 1'
        os.system(cmd)
        if os.path.exists("f.mp4") and os.path.getsize("f.mp4") > 2000000:
            jf = glob.glob("*.json")
            if jf:
                raw_title = json.load(open(jf[0])).get('title','Old Public Domain')
            else:
                raw_title = f"{cat} Old Public Domain No Copyright"
            downloaded = True
            print(f"YT SUCCESS: {raw_title} - {os.path.getsize('f.mp4')} bytes")
    except Exception as e:
        print(f"YT Failed {e}")

# ===== TRY 2: ARCHIVE (100% backup) =====
if not downloaded:
    print("YT failed/blocked, switching to ARCHIVE 100+ Pool")
    random.shuffle(ARCHIVE_FILMS)
    for fid in ARCHIVE_FILMS[:10]: # 10 IDs try karega ek ke baad ek
        print(f"Trying Archive: {fid}")
        os.system(f"wget -q --timeout=120 https://archive.org/download/{fid}/{fid}_512kb.mp4 -O f.mp4 || wget -q --timeout=120 https://archive.org/download/{fid}/{fid}.mp4 -O f.mp4")
        if os.path.exists("f.mp4") and os.path.getsize("f.mp4") > 5000000:
            raw_title = f"{fid} - Old Classic Hindi Film Public Domain No Copyright"
            downloaded = True
            print(f"ARCHIVE SUCCESS: {fid}")
            break
        os.system("rm -f f.mp4")
        time.sleep(1)

if not downloaded or not os.path.exists("f.mp4"):
    print("Both failed")
    exit(1)

# ===== FULL SEO =====
base = raw_title.replace("Full Movie","").strip()[:55]
TITLE = f"{base} | {cat} | Retro Vibe Club"[:65]

DESC = f"""{raw_title}

{cat} | 60+ Years Old | Public Domain | No Copyright | No Owner | Free To Use

Retro Vibe Club pe aap dekh rahe hain purani yaadon ka khazana.

🎬 Category: {cat}
📅 Era: 1940-1970 Old Classic
🔓 License: Public Domain - No Copyright Strike - Free

Rozana {cat} dekhne ke liye Follow karein 🙏

#RetroVibeClub #{cat.replace(' ','')} #PublicDomain #NoCopyright #OldIsGold #OldHindiFilm #PuraneGane #LokSanskriti #VintageIndia #ClassicBollywood #FreeToUse #BhojpuriLokgeet #OldBhajan #Natak #NoOwner #FolkCulture

Keywords: {cat}, old hindi film, public domain, no copyright, retro vibe club, lokgeet, bhajan, natak
"""

# CUT
sp.call(["ffmpeg","-y","-ss","90","-i","f.mp4","-t","90","-c:v","libx264","-preset","ultrafast","-b:v","800k","-c:a","aac","c.mp4"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
if not os.path.exists("c.mp4") or os.path.getsize("c.mp4") < 500000:
    os.system("cp f.mp4 c.mp4")

sp.call(["ffmpeg","-y","-ss","2","-i","c.mp4","-vframes","1","t.jpg"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
print(f"FINAL READY: {os.path.getsize('c.mp4')} bytes")

# UPLOAD
tok=os.environ['FB_PAGE_TOKEN']
r=requests.post("https://graph.facebook.com/v19.0/me/videos", files={'source': open('c.mp4','rb')}, data={'title': TITLE, 'description': DESC, 'access_token': tok}, timeout=180).json()
print(r)
if 'id' in r:
    print(f"✅ UPLOADED ID {r['id']}")
else:
    print("❌ TOKEN EXPIRED - Naya token daalo")
