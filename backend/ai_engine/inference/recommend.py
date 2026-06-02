import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os


def recommend_careers(user_profile_text):

    # Load Dataset
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    DATASET_PATH = os.path.join(
        BASE_DIR,
        "..",
        "datasets",
        "career_master_dataset.csv"
    )

    df = pd.read_csv(DATASET_PATH)

    # Create Career Profile
    df["career_profile"] = (
        df["technical_skills"].astype(str) + " " +
        df["soft_skills"].astype(str) + " " +
        df["interests"].astype(str) + " " +
        df["personality"].astype(str) + " " +
        df["goals"].astype(str)
    )

    # Combine User Profile + Career Profiles
    all_profiles = [user_profile_text] + df["career_profile"].tolist()

    # TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_profiles)

    # User Vector
    user_vector = tfidf_matrix[0]

    # Career Vectors
    career_vectors = tfidf_matrix[1:]

    # Similarity Scores
    similarity_scores = cosine_similarity(
        user_vector,
        career_vectors
    )

    career_scores = []

    for i, score in enumerate(similarity_scores[0]):

        career_scores.append({

    "career": df.iloc[i]["career"],
    "score": float(round(score * 100, 2)),
    "description": df.iloc[i]["description"],
    "career_category": df.iloc[i]["career_category"],
    "salary_range": df.iloc[i]["salary_range"],
    "future_scope": df.iloc[i]["future_scope"],
    "technical_skills": df.iloc[i]["technical_skills"],
    "roadmap": df.iloc[i]["roadmap"]

})

    career_scores = sorted(
        career_scores,
        key=lambda x: x["score"],
        reverse=True
    )

    return career_scores[:5]


# Testing
if __name__ == "__main__":

    user_profile = """
    Python
    Machine Learning
    Data Science
    Problem Solving
    Analytical
    High Salary
    """

    recommendations = recommend_careers(
        user_profile
    )

    print("\nTop 5 Career Recommendations:\n")

    for career in recommendations:
        print(career)