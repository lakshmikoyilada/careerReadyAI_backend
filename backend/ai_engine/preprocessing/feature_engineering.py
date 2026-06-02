import pandas as pd

# Load cleaned dataset
df = pd.read_csv("../datasets/career_dataset_cleaned.csv")

# Create one combined text column
df["combined_text"] = (
    df["Education Level"].astype(str) + " " +
    df["Specialization"].astype(str) + " " +
    df["Skills"].astype(str) + " " +
    df["Certifications"].astype(str)
)

print("Feature Engineering Completed!")

print("\nSample Combined Text:\n")

print(df["combined_text"].head())

# Save dataset
df.to_csv(
    "../datasets/career_dataset_features.csv",
    index=False
)

print("\nDataset saved successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])