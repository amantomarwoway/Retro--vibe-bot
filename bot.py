import requests,random,os,subprocess as sp

def seo(t, cat):
 t=t[:65]
 return t, f"{t}\n\n{cat} | 60+ saal purani public domain recording. Retro Vibe Club par dekho/suno.\n\n#RetroVibeClub #{cat.replace(' ','')} #PublicDomain #OldIsGold #LokSanskriti"

# 100+ Backup ka pool - Search block hua to bhi isme se hi uthayega
# Ye sab Archive.org par maujood hai
LARGE_POOL = {
 "Old Film": ["Kismet1943","Mahal1949","Andaz1949","Barsaat1949","Awaara1951","Deedar1951","Aan1952","Anarkali1953","DoBighaZamin1953","Shree4201955","Devdas1955","CID1956","MotherIndia1957","NayaDaur1957","Madhumati1958","ChaltiKaNaamGaadi1958","Anari1959","Mughal-e-Azam1960","Junglee1961","GangaJumna1961","BeesSaalBaad1962","DilEkMandir1963","Sangam1964","Dosti1964","Leader1964","Arzoo1965"] * 4, # x4 karke 100+ bana diya
 "Bhajan": ["BhajanCollectionOld","HanumanChalisaOld","RamBhajanOldIsGold","ShivBhajanTraditional","KrishnaBhajan1950","GayatriMantraOld","DurgaBhajanFolk","VishnuBhajanCollection"] * 13,
 "Lokgeet": ["BhojpuriLokgeet","HaryanviRagniFolk","RajasthaniMaand","PunjabiMahiyaFolk","BrajHoliLokgeet","BundelkhandiLokgeet","ChhattisgarhiLokgeet","AwadhiLokgeet","BihariChaitaKajari"] * 12,
 "Natak": ["NautankiAmarSingh","RamleelaOld","SwangHarishchandra","BhavaiGujaratiFolk","TamaashaMaharashtra","JatraBengaliFolk","BhandPatherKashmiri"] * 15,
 "Old Songs": ["KLSaigalSongs","RafiOldCollection","LataOld1950s","KishoreKumarOld","MukeshOldSongs","AshaBhosleOld","HemantKumarOld","GeetaDuttOldSongs"] * 13
}

cat = random.choice(list(LARGE_POOL.keys()))
print(f"Category Today: {cat}")

items = []
try:
 qmap = {
  "Old Film":"mediatype:(movies) AND Hindi AND year:[1940 TO 1965]",
  "Bhajan":"mediatype:(audio) AND (Bhajan OR Devotional) AND Hindi",
  "Lokgeet":"mediatype:(audio) AND (Lokgeet OR Folk) AND India",
  "Natak":"mediatype:(movies) AND (Nautanki OR Swang OR Natak)",
  "Old Songs":"mediatype:(audio) AND Old Hindi Film Songs"
 }
 url = f"https://archive.org/advancedsearch.php?q={qmap[cat]}&fl=identifier,title&rows=200&output=json&sort=downloads desc"
 r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=30).json()
 items = r.get('response',{}).get('docs',[])
 print(f"Found {len(items)} from Archive Search")
except Exception as e:
 print(f"Search fail {e}")

# Agar search se 20 se kam aaye to backup se 100 bhar de
if len(items) < 20:
 print("Using LARGE backup pool")
 items = [{"identifier": random.choice(LARGE_POOL[cat]), "title": f"{cat} Classic {random.randint(1940,1965)}"} for _ in range(120)]

# Final random pick
s = random.choice(items)
TITLE,DESC = seo(s.get('title', f"{cat} Old Classic {s['identifier']}"), cat)
id = s['identifier']
print(f"FINAL PICK: {TITLE} -> {id}")

# Download Logic
for ext in ["_512kb.mp4",".mp4","_h.264.mp4","_64kb.mp3",".mp3"]:
 os.system(f"wget -q --user-agent='Mozilla/5.0' https://archive.org/download/{id}/{id}{ext} -O temp_{ext} && mv temp_{ext} f{'mp4' if 'mp4' in ext else 'mp3'} 2>/dev/null || true")
 if os.path.exists("f.mp4") or os.path.exists("f.mp3"): break

if os.path.exists("f.mp4") and os.path.getsize("f.mp4")>100000:
 sp.call(["ffmpeg","-y","-ss","60","-i","f.mp4","-t",str(random.randint(120,300)),"-c:v","libx264","-preset","veryfast","-c:a","aac","c.mp4"],stdout=sp.DEVNULL,stderr=sp.DEVNULL)
elif os.path.exists("f.mp3"):
 sp.call(["ffmpeg","-y","-loop","1","-i","https://i.imgur.com/8Km9tLL.jpg","-i","f.mp3","-t","150","-shortest","-c:v","libx264","-pix_fmt","yuv420p","c.mp4"],stdout=sp.DEVNULL,stderr=sp.DEVNULL)
else:
 # Last fallback - koi bhi film pakka milegi
 os.system("wget -q https://archive.org/download/Kismet1943/Kismet1943_512kb.mp4 -O f.mp4")
 sp.call(["ffmpeg","-y","-ss","120","-i","f.mp4","-t","180","-c:v","libx264","-c:a","aac","c.mp4"],stdout=sp.DEVNULL,stderr=sp.DEVNULL)

sp.call(["ffmpeg","-y","-ss","2","-i","c.mp4","-vframes","1","t.jpg"],stdout=sp.DEVNULL,stderr=sp.DEVNULL)

tok=os.environ['FB_PAGE_TOKEN']
vid=requests.post(f"https://graph.facebook.com/v19.0/me/videos",files={'source':open('c.mp4','rb')},data={'title':TITLE,'description':DESC,'access_token':tok}).json()
print(vid)
