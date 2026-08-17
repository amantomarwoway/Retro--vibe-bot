import os,random,requests,subprocess as sp,time

print("=== BOT START ===")

FILMS = ["Kismet1943","Mahal1949","Awaara1951","Shree4201955","MotherIndia1957","Madhumati1958","Anari1959","Mughal-e-Azam1960","Junglee1961","BeesSaalBaad1962","Sangam1964","Dosti1964"]*9

fid = random.choice(FILMS)
print(f"PICK: {fid}")

os.system("rm -f f.mp4 c.mp4 t.jpg")

mirrors = [
 f"https://archive.org/download/{fid}/{fid}_512kb.mp4",
 f"https://dn1.archive.org/download/{fid}/{fid}_512kb.mp4",
 f"https://ia800200.us.archive.org/0/items/{fid}/{fid}_512kb.mp4",
 f"https://archive.org/download/{fid}/{fid}.mp4"
]

ok = False
for url in mirrors:
    print(f"DOWNLOADING: {url}")
    os.system(f"curl -L -A 'Mozilla/5.0' --connect-timeout 30 --max-time 180 -o f.mp4 '{url}' -s")
    if os.path.exists("f.mp4"):
        sz = os.path.getsize("f.mp4")
        print(f"Got {sz} bytes")
        if sz > 5000000:
            ok = True
            break
        else:
            os.system("rm -f f.mp4")
    time.sleep(1)

if not ok:
    print("ALL MIRRORS FAILED")
    exit(1)

raw = f"{fid} Old Classic Hindi Film Public Domain No Copyright"
TITLE = f"{raw[:45]} | Retro Vibe Club"[:65]
DESC = f"{raw}\n\nOld Classic | Public Domain | No Copyright | No Owner\n\n#RetroVibeClub #OldFilm #PublicDomain #NoCopyright #OldIsGold #VintageIndia"

print("CUTTING 90 sec...")
res = sp.call(["ffmpeg","-y","-ss","90","-i","f.mp4","-t","90","-c:v","libx264","-preset","ultrafast","-b:v","800k","-c:a","aac","c.mp4"])
if res != 0 or not os.path.exists("c.mp4") or os.path.getsize("c.mp4") < 100000:
    os.system("cp f.mp4 c.mp4")

print(f"FINAL c.mp4 = {os.path.getsize('c.mp4')} bytes")

tok = os.environ.get('FB_PAGE_TOKEN','')
r = requests.post("https://graph.facebook.com/v19.0/me/videos", files={'source': open('c.mp4','rb')}, data={'title': TITLE, 'description': DESC, 'access_token': tok}, timeout=180)
print(r.text)
if 'id' in r.json():
    print(f"SUCCESS ID {r.json()['id']}")
