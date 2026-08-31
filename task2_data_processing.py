"""
TrendPulse - Task 2: Data Processing
Needs: data/trends_YYYYMMDD.json from Task 1
"""

import pandas as pd
import os
import glob

# Step 1 - Load JSON
json_files = glob.glob("data/trends_*.json")
if not json_files:
    print("No JSON file found. Run Task 1 first!")
    exit()

json_path = sorted(json_files)[-1]
df = pd.read_json(json_path)
print(f"Loaded {len(df)} stories from {json_path}")

# Step 2 - Clean Data
df = df.drop_duplicates(subset=["post_id"], keep="first")
print(f"After removing duplicates: {len(df)}")

df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)

df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

df["title"] = df["title"].astype(str).str.strip()
print(f"\nTotal after cleaning: {len(df)} rows remaining")

# Step 3 - Save as CSV
os.makedirs("data", exist_ok=True)
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")
print("\nStories per category:")
print(df["category"].value_counts().to_string())
