"""
TrendPulse - Task 4: Visualization with Matplotlib
Needs: data/trends_analysed.csv from Task 3
Author: Rajeshwari
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------- 1. Setup (2 marks) --------------------
# Load analysed CSV from Task 3
input_file = "data/trends_analysed.csv"

if not os.path.exists(input_file):
    print(f"Error: {input_file} not found. Please run Task 3 first.")
    exit()

df = pd.read_csv(input_file)
print(f"Loaded {len(df)} stories from {input_file}")

# Create outputs folder if not exists
os.makedirs("outputs", exist_ok=True)

# Set style for better charts
plt.style.use('default')

# -------------------- 2. Chart 1: Top 10 Stories by Score (6 marks) --------------------
# Get top 10 stories sorted by score descending
top10 = df.sort_values(by="score", ascending=False).head(10)

# Shorten titles longer than 50 chars for y-axis readability
# Example: "This is a very long title..." -> "This is a very long title that is more than..."
def shorten_title(title):
    if len(title) > 50:
        return title[:47] + "..."
    return title

top10["short_title"] = top10["title"].apply(shorten_title)

plt.figure(figsize=(10, 6))
# Horizontal bar chart - y=title, x=score
plt.barh(top10["short_title"][::-1], top10["score"][::-1], color="skyblue")
plt.xlabel("Score (Upvotes)")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.tight_layout()
# IMPORTANT: savefig before show
plt.savefig("outputs/chart1_top_stories.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved outputs/chart1_top_stories.png")

# -------------------- 3. Chart 2: Stories per Category (6 marks) --------------------
# Count stories per category
category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 5))
# Different colour for each bar - using colormap
colors = plt.cm.Set3(range(len(category_counts)))

plt.bar(category_counts.index, category_counts.values, color=colors)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.xticks(rotation=15) # Rotate labels if many categories
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved outputs/chart2_categories.png")

# -------------------- 4. Chart 3: Score vs Comments Scatter (6 marks) --------------------
plt.figure(figsize=(8, 6))

# Separate popular vs non-popular for different colours
popular = df[df["is_popular"] == True]
non_popular = df[df["is_popular"] == False]

# Scatter plot with two colours
plt.scatter(non_popular["score"], non_popular["num_comments"],
            c="gray", alpha=0.6, label="Not Popular", s=50)
plt.scatter(popular["score"], popular["num_comments"],
            c="red", alpha=0.7, label="Popular", s=60)

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved outputs/chart3_scatter.png")

# -------------------- Bonus: Dashboard (3 marks) --------------------
# Combine all 3 charts into one figure using subplots(1,3)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("TrendPulse Dashboard", fontsize=16, fontweight="bold")

# Dashboard Chart 1 - Top 10
axes[0].barh(top10["short_title"][::-1], top10["score"][::-1], color="skyblue")
axes[0].set_xlabel("Score")
axes[0].set_title("Top 10 by Score")
axes[0].tick_params(labelsize=7)

# Dashboard Chart 2 - Categories
axes[1].bar(category_counts.index, category_counts.values, color=colors)
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Count")
axes[1].set_title("Stories per Category")
axes[1].tick_params(axis='x', rotation=20, labelsize=8)

# Dashboard Chart 3 - Scatter
axes[2].scatter(non_popular["score"], non_popular["num_comments"],
                c="gray", alpha=0.6, label="Not Popular", s=20)
axes[2].scatter(popular["score"], popular["num_comments"],
                c="red", alpha=0.7, label="Popular", s=25)
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].set_title("Score vs Comments")
axes[2].legend(fontsize=8)

plt.tight_layout()
plt.savefig("outputs/dashboard.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved outputs/dashboard.png (Bonus)")

print("\nAll charts saved in outputs/ folder!")
