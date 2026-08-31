import requests, json, os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

headers = {"User-Agent": "TrendPulse/1.0"}

categories = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

session = requests.Session()
session.headers.update(headers)

# 1. Get IDs
top_ids = session.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=15).json()[:200] # 200 enough, 500 too much

def fetch_story(sid):
    try:
        r = session.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=8)
        return r.json()
    except:
        return None

stories = []
counts = {c:0 for c in categories}

# 2. Fetch in parallel - 10x faster
with ThreadPoolExecutor(max_workers=20) as executor:
    future_to_id = {executor.submit(fetch_story, sid): sid for sid in top_ids}

    for future in as_completed(future_to_id):
        story = future.result()
        if not story or not story.get("title"):
            continue

        title_lower = story.get("title","").lower()

        for cat, kws in categories.items():
            if counts[cat] >= 25: continue
            if any(kw.lower() in title_lower for kw in kws):
                stories.append({
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": cat,
                    "score": story.get("score",0),
                    "num_comments": story.get("descendants",0),
                    "author": story.get("by",""),
                    "collected_at": datetime.now().isoformat()
                })
                counts[cat] += 1
                break

        if all(v >= 25 for v in counts.values()):
            # cancel remaining futures
            for f in future_to_id: f.cancel()
            break

os.makedirs("data", exist_ok=True)
path = f"data/trends_{datetime.now():%Y%m%d}.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(stories, f, indent=4, ensure_ascii=False)

print(f"Collected {len(stories)} -> {path} {counts}")