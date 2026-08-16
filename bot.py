import requests,random,os,subprocess as sp
def seo(t):
 t=t[:55];d=f"{t} - 60+ saal purani public domain film, copyright-free. Retro Vibe par dekho."[:145]
 return t,f"{t}\n\n{d}\n\n#RetroVibeClub #PublicDomain #OldIsGold #DeshbhaktiGeet"
q='language:Hindi AND year:[1900 TO 1964]'
r=requests.get(f"https://archive.org/advancedsearch.php?q={q}&fl=identifier,title&rows=1000&output=json",timeout=20).json()
items=r['response']['docs'] or [{"identifier":"Kismet1943","title":"Kismet 1943 Classic"}]
s=random.choice(items);TITLE,DESC=seo(s['title']);print(TITLE)
id=s['identifier']
os.system(f"wget -q https://archive.org/download/{id}/{id}_512kb.mp4 -O f.mp4||wget -q https://archive.org/download/{id}/{id}.mp4 -O f.mp4||wget -q https://archive.org/download/{id}/{id}.mp3 -O f.mp3")
if os.path.exists("f.mp4"):
    try: dur=float(sp.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1","f.mp4"]))
    except: dur=700
    if dur>420:
        cut=random.randint(120,420)
        ss=random.randint(300, max(301,int(dur-cut-10)))
        sp.call(["ffmpeg","-y","-ss",str(ss),"-i","f.mp4","-t",str(cut),"-c:v","libx264","-c:a","aac","-aspect","16:9","c.mp4"],stdout=sp.DEVNULL,stderr=sp.DEVNULL)
    else:
        sp.call(["ffmpeg","-y","-i","f.mp4","-c:v","libx264","-c:a","aac","-aspect","16:9","c.mp4"],stdout=sp.DEVNULL,stderr=sp.DEVNULL)
    sp.call(["ffmpeg","-y","-ss","2","-i","c.mp4","-vframes","1","t.jpg"],stdout=sp.DEVNULL,stderr=sp.DEVNULL)
else:
    sp.call(["ffmpeg","-y","-loop","1","-i","https://i.imgur.com/8Km9tLL.jpg","-i","f.mp3","-t","90","-shortest","c.mp4"],stdout=sp.DEVNULL,stderr=sp.DEVNULL)
tok=os.environ['FB_PAGE_TOKEN']
vid=requests.post(f"https://graph.facebook.com/v19.0/me/videos",files={'source':open('c.mp4','rb')},data={'title':TITLE,'description':DESC,'access_token':tok}).json()
print(vid)
try:requests.post(f"https://graph.facebook.com/v19.0/{vid['id']}/thumbnails",files={'source':open('t.jpg','rb')},data={'is_preferred':'true','access_token':tok})
except:pass
