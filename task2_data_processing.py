```python
import pandas as pd
import glob
import os


# --------------------------------------------------
# Step 1: Find the JSON file inside the data folder
# --------------------------------------------------

json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No trends JSON file found in the data folder.")
    exit()

# Use the first trends JSON file found
input_file = json_files[0]


# --------------------------------------------------
# Step 2: Load the JSON file into a DataFrame
# --------------------------------------------------

df = pd.read_json(input_file)

print(f"Loaded {len(df)} stories from {input_file}")


# --------------------------------------------------
# Step 3: Remove duplicate stories
# --------------------------------------------------

df = df.drop_duplicates(subset="post_id")

print(f"After removing duplicates: {len(df)}")


# --------------------------------------------------
# Step 4: Remove rows with missing required values
# --------------------------------------------------

df = df.dropna(
    subset=["post_id", "title", "score"]
)

print(f"After removing nulls: {len(df)}")


# --------------------------------------------------
# Step 5: Convert score and num_comments to integers
# --------------------------------------------------

df["score"] = pd.to_numeric(
    df["score"],
    errors="coerce"
)

df["num_comments"] = pd.to_numeric(
    df["num_comments"],
    errors="coerce"
)

# Remove rows that became missing after conversion
df = df.dropna(
    subset=["score", "num_comments"]
)

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)


# --------------------------------------------------
# Step 6: Remove low-quality stories
# Score must be at least 5
# --------------------------------------------------

df = df[df["score"] >= 5]

print(f"After removing low scores: {len(df)}")


# --------------------------------------------------
# Step 7: Remove extra whitespace from titles
# --------------------------------------------------

df["title"] = df["title"].str.strip()


# --------------------------------------------------
# Step 8: Save the cleaned DataFrame as CSV
# --------------------------------------------------

output_file = "data/trends_clean.csv"

df.to_csv(
    output_file,
    index=False
)

print(f"\nSaved {len(df)} rows to {output_file}")


# --------------------------------------------------
# Step 9: Print stories per category
# --------------------------------------------------

print("\nStories per category:")

category_counts = df["category"].value_counts()

for category, count in category_counts.items():
    print(f"  {category:<15} {count}")
```

