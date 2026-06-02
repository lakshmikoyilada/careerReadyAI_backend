import pandas as pd

# Load original dataset
df = pd.read_csv("../datasets/career_dataset.csv")

# Careers we want to keep
tech_careers = [
    "Software Engineer",
    "ML Engineer",
    "Research Scientist",
    "Business Analyst"
]

# Filter dataset
filtered_df = df[df["Recommended Career"].isin(tech_careers)]

# Save new dataset
filtered_df.to_csv(
    "../datasets/career_dataset_filtered.csv",
    index=False
)

print("Filtered dataset created successfully!")
print("Rows:", filtered_df.shape[0])
print("Columns:", filtered_df.shape[1])

print("\nCareer Distribution:")
print(filtered_df["Recommended Career"].value_counts())