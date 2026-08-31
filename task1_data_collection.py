import requests
import json
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

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

TARGET_PER_CAT = 25
MAX_IDS = 250 # 250 is enough to get 125 stories

print("Fetching top story IDs...")
top_ids = session.get(
    "https://hacker-news.firebaseio.com/v0/topstories.json",
    timeout=15
).json()[:MAX_IDS]

def fetch_story(sid):
    try:
        r = session.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

stories = []
counts = {c: 0 for c in categories}

print(f"Fetching {len(top_ids)} stories in parallel...")
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(fetch_story, sid): sid for sid in top_ids}

    for future in as_completed(futures):
        story = future.result()
        if not story or not story.get("title"):
            continue

        title_lower = story.get("title","").lower()

        for cat, keywords in categories.items():
            if counts[cat] >= TARGET_PER_CAT:
                continue
            if any(k.lower() in title_lower for k in keywords):
                stories.append({
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": cat,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", ""),
                    "url": story.get("url", ""),
                    "collected_at": datetime.now().isoformat()
                })
                counts[cat] += 1
                break

        if all(v == TARGET_PER_CAT for v in counts.values()):
            break

# Sort by category for neatness
stories.sort(key=lambda x: x['category'])

os.makedirs("data", exist_ok=True)
date_str = datetime.now().strftime("%Y%m%d")
file_path = f"data/trends_{date_str}.json"

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(stories, f, indent=4, ensure_ascii=False)

print(f"✅ Collected {len(stories)} stories | {counts}")
print(f"Saved to {file_path}")