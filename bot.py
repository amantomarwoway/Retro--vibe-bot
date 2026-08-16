import requests,random,os,subprocess as sp

def seo(t, cat):
    return t[:65], f"{t}\n\n{cat} | Retro Vibe Club - Purani Yaadein\n\n#RetroVibeClub #{cat.replace(' ','')} #PublicDomain #OldIsGold"

# 100+ POOL (fast download wale hi rakhe hai - sab 50-150MB ke andar)
POOL = {
 "Old Film": ["Kismet1943","Mahal1949","Barsaat1949","Awaara1951","Aan1952","Anarkali1953","Shree4201955","CID1956","MotherIndia1957","Madhumati1958","Anari1959","Mughal-e-Azam1960","Junglee1961","BeesSaalBaad1962","Sangam1964","Dosti1964"] * 7,
 "Bhajan": ["bhajan"] * 100, # search se ayega
 "Lokgeet": ["lokgeet"] * 100,
 "Natak": ["nautanki"] * 100,
 "Old Songs": ["old hindi song"] * 100
}

cat = random.choice(["Old Film","Old Film","Old Film","Bhajan","Lokgeet","Natak","Old Songs"])
print(f"TODAY: {cat}")

# Try fast search - sirf 30 sec ka timeout
items = []
try:
    q = {
     "Old Film": "mediatype:movies AND Hindi AND year:[1940 TO 1964]",
     "Bhajan": "mediatype:audio AND Bhajan",
     "Lokgeet": "mediatype:audio AND Lokgeet",
     "Natak": "mediatype:movies AND Nautanki",
     "Old Songs": "mediatype:audio AND Old Hindi Songs"
    }[cat]
    r = requests.get(f"https://archive.org/advancedsearch.php?q={q}&fl=identifier,title&rows=50&output=json", headers={'User-Agent':'Mozilla/5.0'}, timeout=15).json()
    items = r.get('response',{}).get('docs',[])
    print(f"Search found {len(items)}")
except:
    print("Search fail, using fast backup")

if len(items) < 5:
    # Fast backup - pakka chalne wali IDs
    fast_ids = ["Kismet1943","Mahal1949","Shree4201955","MotherIndia1957","Mughal-e-Azam1960","Awaara1951","Barsaat1949","CID1956"]
    fid = random.choice(fast_ids)
    items = [{"identifier": fid, "title": f"{fid} - {cat} Classic"}]

s = random.choice(items)
id = s['identifier']
title = s.get('title', id)
TITLE, DESC = seo(title, cat)
print(f"PICK: {TITLE} -> {id}")

# CLEAN OLD FILES
os.system("rm -f f.mp4 f.mp3 c.mp4 t.jpg temp*")

# FAST DOWNLOAD - sirf 512kb wala, 2 min timeout ke saath
os.system(f"timeout 90 wget -q --tries=1 https://archive.org/download/{id}/{id}_512kb.mp4 -O f.mp4 || timeout 90 wget -q --tries=1 https://archive.org/download/{id}/{id}.mp4 -O f.mp4 || timeout 90 wget -q --tries=1 https://archive.org/download/{id}/{id}.mp3 -O f.mp3")

# Agar abhi bhi nahi aaya to Kismet pakka hai
if not os.path.exists("f.mp4") and not os.path.exists("f.mp3"):
    print("Fallback to Kismet")
    os.system("timeout 90 wget -q https://archive.org/download/Kismet1943/Kismet1943_512kb.mp4 -O f.mp4")
    TITLE = "Kismet 1943 - Old Classic Film"
    DESC = "Kismet 1943 #RetroVibeClub #OldIsGold"

# SUPERFAST CUT - 90 sec ka clip, ultrafast
if os.path.exists("f.mp4"):
    sp.call(["ffmpeg","-y","-ss","100","-i","f.mp4","-t","90","-c:v","libx264","-preset","ultrafast","-b:v","700k","-c:a","aac","-b:a","96k","c.mp4"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
else:
    sp.call(["ffmpeg","-y","-loop","1","-i","https://i.imgur.com/8Km9tLL.jpg","-i","f.mp3","-t","90","-shortest","-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p","c.mp4"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)

sp.call(["ffmpeg","-y","-ss","1","-i","c.mp4","-vframes","1","t.jpg"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)

# UPLOAD
tok = os.environ['FB_PAGE_TOKEN']
print("Uploading to FB...")
vid = requests.post(f"https://graph.facebook.com/v19.0/me/videos", files={'source': open('c.mp4','rb')}, data={'title': TITLE, 'description': DESC, 'access_token': tok}, timeout=60).json()
print(vid)

if 'id' in vid and os.path.exists("t.jpg"):
    try:
        requests.post(f"https://graph.facebook.com/v19.0/{vid['id']}/thumbnails", files={'source': open('t.jpg','rb')}, data={'is_preferred':'true','access_token': tok}, timeout=30)
    except:
        pass
