import pandas as pd

df = pd.read_csv(
    "../datasets/career_dataset.csv"
)

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nCareer Distribution:")
print(df['Recommended Career'].value_counts())

print("\nSample Rows:")
print(df.head())

print("\nTotal Unique Careers:")
print(df['Recommended Career'].nunique())

print("\nCareer Names:")
print(df['Recommended Career'].unique())