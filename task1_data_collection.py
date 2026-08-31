"""
TrendPulse - Task 1: Data Collection
Fetches trending stories from HackerNews API and categorizes them
Author: Rajeshwari
"""
import requests
import time
import json
import os
from datetime import datetime

# Required header as per task
headers = {"User-Agent": "TrendPulse/1.0"}

# Category keywords to match (case-insensitive)
categories = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

# Step 1 - Get top 500 story IDs
url = "https://hacker-news.firebaseio.com/v0/topstories.json"

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    story_ids = response.json()[:500] # Fetch first 500 as per task
    print(f"Fetched {len(story_ids)} top story IDs")
except Exception as e:
    print(f"Failed to fetch top stories: {e}")
    story_ids = []

stories = []
category_count = {category: 0 for category in categories}

# Step 2 - We need to check each story and assign category
# Task says: Wait 2 seconds between each category (one sleep per category loop)
# So we will loop categories one by one

for category, keywords in categories.items():
    print(f"\nCollecting for category: {category}...")

    # If already have 25 for this category, skip
    if category_count[category] >= 25:
        continue

    for story_id in story_ids:
        # Stop if we already have 25 for this current category
        if category_count[category] >= 25:
            break

        # Stop if we have collected 125 total (25*5)
        if sum(category_count.values()) >= 125:
            break

        try:
            # Fetch each story details
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            res = requests.get(item_url, headers=headers, timeout=10)
            res.raise_for_status()
            story = res.json()

            if not story or not story.get("title"):
                continue

            title = story.get("title", "")
            title_lower = title.lower()

            # Check if title contains any keyword for THIS category
            if any(keyword.lower() in title_lower for keyword in keywords):
                # Check if this story already collected (avoid duplicates)
                if any(s["post_id"] == story.get("id") for s in stories):
                    continue

                # Extract required 7 fields
                stories.append({
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", ""),
                    "collected_at": datetime.now().isoformat()
                })
                category_count[category] += 1

        except Exception as e:
            # If request fails, print and move on - don't crash
            print(f"Failed to fetch story {story_id}: {e}")
            continue

    # Wait 2 seconds between each category as per task requirement
    print(f"Collected {category_count[category]} for {category}. Waiting 2 sec...")
    time.sleep(2)

# Step 3 - Save to JSON file
os.makedirs("data", exist_ok=True)

date_string = datetime.now().strftime("%Y%m%d")
file_path = f"data/trends_{date_string}.json"

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(stories, file, indent=4, ensure_ascii=False)

# Expected output format
print(f"\nCollected {len(stories)} stories. Saved to {file_path}")
print(f"Breakdown: {category_count}")