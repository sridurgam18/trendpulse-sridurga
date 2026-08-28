
import requests
import time
import json
import os
from datetime import datetime

# User-Agent for Hacker News requests
headers = {"User-Agent": "TrendPulse/1.0"}

# Keywords used to identify each category
keywords = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],

    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],

    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game",
        "team", "player", "league", "championship"
    ],

    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "NASA", "genome"
    ],

    "entertainment": [
        "movie", "film", "music", "Netflix",
        "game", "book", "show", "award", "streaming"
    ]
}


# --------------------------------------------------
# Categorize a story based on keywords in its title
# --------------------------------------------------

def categorize(title):
    title = title.lower()

    for category, words in keywords.items():
        for word in words:
            if word.lower() in title:
                return category

    return None


# --------------------------------------------------
# Step 1: Fetch top story IDs
# --------------------------------------------------

try:
    response = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json",
        headers=headers
    )

    response.raise_for_status()

    # Take a large number of top stories
    story_ids = response.json()[:1000]

except requests.RequestException as e:
    print("Failed to fetch story IDs:", e)
    story_ids = []


# --------------------------------------------------
# Step 2: Create counters and result list
# --------------------------------------------------

category_count = {
    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}

collected_stories = []


# --------------------------------------------------
# Step 3: Process each category
# --------------------------------------------------

for category in keywords:

    # Stop if we already have 100 stories
    if len(collected_stories) >= 100:
        break

    # Check every top story ID
    for story_id in story_ids:

        # Stop this category after 25 stories
        if category_count[category] >= 25:
            break

        try:
            url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

            response = requests.get(
                url,
                headers=headers
            )

            response.raise_for_status()

            story = response.json()

            if not story:
                continue

            title = story.get("title", "")

            # Check whether this story belongs to this category
            assigned_category = categorize(title)

            if assigned_category != category:
                continue

            # Create the required 7 fields
            record = {
                "post_id": story.get("id"),
                "title": title,
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by"),
                "collected_at": datetime.now().isoformat()
            }

            collected_stories.append(record)

            category_count[category] += 1

        except requests.RequestException as e:
            print(f"Failed to fetch story {story_id}: {e}")
            continue

    # Wait 2 seconds BETWEEN categories
    #print(category, category_count[category])
    time.sleep(2)


# --------------------------------------------------
# Step 4: Create data folder
# --------------------------------------------------

os.makedirs("data", exist_ok=True)


# --------------------------------------------------
# Step 5: Create today's filename
# --------------------------------------------------

date_string = datetime.now().strftime("%Y%m%d")

filename = f"data/trends_{date_string}.json"


# --------------------------------------------------
# Step 6: Save stories to JSON
# --------------------------------------------------

with open(filename, "w", encoding="utf-8") as f:
    json.dump(
        collected_stories,
        f,
        indent=2,
        ensure_ascii=False
    )


# --------------------------------------------------
# Step 7: Print final result
# --------------------------------------------------

print(
    f"Collected {len(collected_stories)} stories. "
    f"Saved to {filename}"
)

