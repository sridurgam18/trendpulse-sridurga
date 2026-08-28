
import pandas as pd
import numpy as np

# Load the clean CSV file from Task 2
df = pd.read_csv("data/trends_clean.csv")

# Print the shape of the DataFrame
print("Loaded data:", df.shape)

# Print the first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Calculate average score and average comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print(f"\nAverage score   : {average_score:.2f}")
print(f"Average comments: {average_comments:.2f}")


# -------------------------------
# NumPy Analysis
# -------------------------------

# Convert score column to NumPy array
scores = df["score"].to_numpy()

# Mean, median and standard deviation
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

# Highest and lowest score
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")


# Find the category with the most stories
category_counts = df["category"].value_counts()

most_category = category_counts.idxmax()
most_category_count = category_counts.max()

print(
    f"\nMost stories in: "
    f"{most_category} ({most_category_count} stories)"
)


# Find the story with the most comments
most_comments_index = np.argmax(
    df["num_comments"].to_numpy()
)

most_comments_title = df.loc[
    most_comments_index, "title"
]

most_comments_count = df.loc[
    most_comments_index, "num_comments"
]

print(
    f'\nMost commented story: '
    f'"{most_comments_title}" — '
    f'{most_comments_count} comments'
)


# -------------------------------
# Add New Columns
# -------------------------------

# Engagement = comments divided by score + 1
df["engagement"] = (
    df["num_comments"] / (df["score"] + 1)
)

# True if score is greater than the average score
df["is_popular"] = df["score"] > average_score


# -------------------------------
# Save the result
# -------------------------------

output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")


