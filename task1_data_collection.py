import requests
import time
import json
import os
from datetime import datetime

headers = {"User-Agent": "TrendPulse/1.0"}

# Category keywords
categories = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

# Get the top 500 HackerNews story IDs
url = "https://hacker-news.firebaseio.com/v0/topstories.json"

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    story_ids = response.json()[:500]
except Exception as e:
    print("Failed to fetch top stories:", e)
    story_ids = []

stories = []
category_count = {category: 0 for category in categories}

# Fetch each story and assign a category
for story_id in story_ids:
    try:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        response = requests.get(item_url, headers=headers, timeout=10)
        response.raise_for_status()
        story = response.json()

        title = story.get("title", "")
        title_lower = title.lower()

        selected_category = None

        for category, keywords in categories.items():
            if any(keyword.lower() in title_lower for keyword in keywords):
                selected_category = category
                break

        if selected_category is not None:
            if category_count[selected_category] < 25:
                stories.append({
                    "post_id": story.get("id"),
                    "title": title,
                    "category": selected_category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", ""),
                    "collected_at": datetime.now().isoformat()
                })

                category_count[selected_category] += 1

        # Stop once all five categories have 25 stories
        if all(count == 25 for count in category_count.values()):
            break

    except Exception as e:
        print(f"Failed to fetch story {story_id}:", e)
        continue

# Create data folder if it does not exist
os.makedirs("data", exist_ok=True)

# Create today's filename
date_string = datetime.now().strftime("%Y%m%d")
file_path = f"data/trends_{date_string}.json"

# Save the collected stories
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(stories, file, indent=4, ensure_ascii=False)

print(f"Collected {len(stories)} stories. Saved to {file_path}")