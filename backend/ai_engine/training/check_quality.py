import pandas as pd

df = pd.read_csv("../datasets/career_dataset_features.csv")

for career in df["Recommended Career"].unique():
    print("\n" + "="*50)
    print("CAREER:", career)

    sample = df[df["Recommended Career"] == career].head(5)

    print(sample[[
        "Specialization",
        "Skills",
        "Recommended Career"
    ]])