import os, random, subprocess as sp
print("=== FINAL APP BOT ===")

VIDEOS = {
    "Bhajan": ["https://www.youtube.com/watch?v=4VnL0V5_3qE", "https://www.youtube.com/watch?v=lTRiuFIWV54"],
    "Lokgeet": ["https://www.youtube.com/watch?v=OPf0YbXqDm0", "https://www.youtube.com/watch?v=09R8_2nJtjg"],
    "Natak": ["https://www.youtube.com/watch?v=3SsK-cxlj_w"],
    "Music": ["https://www.youtube.com/watch?v=Q0oIoR1hXz0", "https://www.youtube.com/watch?v=5qap5aO4i9A"],
    "Old Movie": ["https://www.youtube.com/watch?v=4jnEBs74Vuk", "https://www.youtube.com/watch?v=8UVNT4wvIGY"]
}

cat = random.choice(list(VIDEOS.keys()))
url = random.choice(VIDEOS[cat])
print(f"PICKED {cat}: {url}")

sp.run(["yt-dlp","-f","best[height<=720]","--merge-output-format","mp4","-o","input.mp4",url], check=True)
print("DOWNLOAD OK")

sp.run(["ffmpeg","-y","-i","input.mp4","-t","90","-vf","scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:(ow-iw)/2:(oh-ih)/2","-c:v","libx264","-preset","fast","-crf","22","-c:a","aac","final_4k.mp4"], check=True)

import requests
tok=os.environ.get('FB_PAGE_TOKEN','')
title=f"{cat} | No Copyright 4K | Retro Vibe Club"
desc=f"{cat} No Copyright\n#PublicDomain #{cat} #NoCopyright #RetroVibeClub #4KVideo"
if tok:
    with open('final_4k.mp4','rb') as f:
        r=requests.post("https://graph.facebook.com/v19.0/me/videos",files={'source':f},data={'title':title,'description':desc,'access_token':tok},timeout=600)
        print(r.text)
