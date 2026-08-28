
import pandas as pd
import numpy as np


# --------------------------------------------------
# Step 1: Load the clean CSV file
# --------------------------------------------------

input_file = "data/trends_clean.csv"

df = pd.read_csv(input_file)

print("Loaded data:", df.shape)


# --------------------------------------------------
# Step 2: Print the first 5 rows
# --------------------------------------------------

print("\nFirst 5 rows:")
print(df.head())


# --------------------------------------------------
# Step 3: Calculate average score and comments
# --------------------------------------------------

average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print(f"\nAverage score   : {average_score:.2f}")
print(f"Average comments: {average_comments:.2f}")


# --------------------------------------------------
# Step 4: Convert score column to NumPy array
# --------------------------------------------------

scores = df["score"].to_numpy()


# --------------------------------------------------
# Step 5: NumPy statistics
# --------------------------------------------------

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

highest_score = np.max(scores)
lowest_score = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {highest_score}")
print(f"Min score    : {lowest_score}")


# --------------------------------------------------
# Step 6: Find category with most stories
# --------------------------------------------------

category_counts = df["category"].value_counts()

most_common_category = category_counts.idxmax()
most_common_count = category_counts.max()

print(
    f"\nMost stories in: "
    f"{most_common_category} ({most_common_count} stories)"
)


# --------------------------------------------------
# Step 7: Find the story with most comments
# --------------------------------------------------

most_commented_index = df["num_comments"].idxmax()

most_commented_title = df.loc[
    most_commented_index, "title"
]

most_commented_count = df.loc[
    most_commented_index, "num_comments"
]

print(
    f'\nMost commented story: '
    f'"{most_commented_title}" — '
    f'{most_commented_count} comments'
)


# --------------------------------------------------
# Step 8: Add engagement column
# Formula:
# num_comments / (score + 1)
# --------------------------------------------------

df["engagement"] = (
    df["num_comments"] / (df["score"] + 1)
)


# --------------------------------------------------
# Step 9: Add is_popular column
# True if score is greater than average score
# --------------------------------------------------

df["is_popular"] = df["score"] > average_score


# --------------------------------------------------
# Step 10: Save the analysed DataFrame
# --------------------------------------------------

output_file = "data/trends_analysed.csv"

df.to_csv(
    output_file,
    index=False
)

print(f"\nSaved to {output_file}")
