import pandas as pd

# Load filtered dataset
df = pd.read_csv("../datasets/career_dataset_filtered.csv")

print("Before Cleaning:")
print(df.isnull().sum())

# Fill missing certifications
df["Certifications"] = df["Certifications"].fillna("None")

# Save cleaned dataset
df.to_csv(
    "../datasets/career_dataset_cleaned.csv",
    index=False
)

print("\nAfter Cleaning:")
print(df.isnull().sum())

print("\nCleaned dataset saved successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])