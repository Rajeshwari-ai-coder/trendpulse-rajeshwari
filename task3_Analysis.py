"""
TrendPulse - Task 3: Analysis with Pandas & NumPy
Needs: data/trends_clean.csv from Task 2
Author: Rajeshwari
"""

import pandas as pd
import numpy as np
import os

# -------------------- 1. Load and Explore (4 marks) --------------------
# Load the cleaned CSV from Task 2
input_file = "data/trends_clean.csv"

if not os.path.exists(input_file):
    print(f"Error: {input_file} not found. Please run Task 2 first.")
    exit()

df = pd.read_csv(input_file)

# Print shape - (rows, columns)
print(f"Loaded data: {df.shape}")

# Print first 5 rows to see data
print("\nFirst 5 rows:")
print(df.head().to_string())

# Print average score and average num_comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:.0f}")
print(f"Average comments: {avg_comments:.0f}")

# -------------------- 2. Basic Analysis with NumPy (8 marks) --------------------
print("\n--- NumPy Stats ---")

# Using NumPy for stats on score column
# Mean - average of all scores
mean_score = np.mean(df["score"])
print(f"Mean score   : {mean_score:.0f}")

# Median - middle value when sorted
median_score = np.median(df["score"])
print(f"Median score : {median_score:.0f}")

# Std deviation - how spread out scores are
std_score = np.std(df["score"])
print(f"Std deviation: {std_score:.0f}")

# Max and Min score
max_score = np.max(df["score"])
min_score = np.min(df["score"])
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# Which category has most stories? - use value_counts
category_counts = df["category"].value_counts()
most_common_cat = category_counts.idxmax()
most_common_count = category_counts.max()
print(f"\nMost stories in: {most_common_cat} ({most_common_count} stories)")

# Which story has most comments?
# idxmax gives index of max comments
max_comment_idx = df["num_comments"].idxmax()
most_commented = df.loc[max_comment_idx]
print(f"\nMost commented story: \"{most_commented['title']}\"  — {most_commented['num_comments']} comments")

# -------------------- 3. Add New Columns (5 marks) --------------------

# engagement = num_comments / (score + 1)
# +1 to avoid divide by zero, shows discussion per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = True if score > average score, else False
# Using numpy where for boolean column
df["is_popular"] = np.where(df["score"] > avg_score, True, False)

print(f"\nAdded 2 new columns: engagement, is_popular")
print(f"Popular stories: {df['is_popular'].sum()} out of {len(df)}")

# -------------------- 4. Save the Result (3 marks) --------------------
os.makedirs("data", exist_ok=True)
output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")
