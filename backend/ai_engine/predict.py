import os
import joblib
from scipy.sparse import hstack


# =========================
# GET CURRENT DIRECTORY
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================
# LOAD MODEL FILES
# =========================

model = joblib.load(
    os.path.join(BASE_DIR, "models", "career_model.pkl")
)

label_encoder = joblib.load(
    os.path.join(BASE_DIR, "models", "label_encoder.pkl")
)

tfidf = joblib.load(
    os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")
)


# =========================
# PREDICTION FUNCTION
# =========================

def predict_career(user_data):

    combined_text = (
        str(user_data["education_level"]) + " " +
        str(user_data["specialization"]) + " " +
        str(user_data["skills"]) + " " +
        str(user_data["certifications"])
    )

    # Convert text into TF-IDF features
    text_features = tfidf.transform([combined_text])

    # Numeric feature
    numeric_feature = [[user_data["cgpa_percentage"]]]

    # Combine both features
    final_features = hstack([text_features, numeric_feature])

    # Get probability scores
    probabilities = model.predict_proba(final_features)[0]

    # Get top 5 predictions
    top_indices = probabilities.argsort()[-5:][::-1]

    recommended_careers = []

    for index in top_indices:

        career_name = label_encoder.inverse_transform([index])[0]

        score = float(round(probabilities[index] * 100, 2))

        recommended_careers.append({
            "career": career_name,
            "score": score
        })

    return recommended_careers


# =========================
# TEST PREDICTION
# =========================

if __name__ == "__main__":

    sample_user = {
        "education_level": "Bachelor's",
        "specialization": "Computer Science",
        "skills": "Python, SQL, Machine Learning",
        "certifications": "AWS",
        "cgpa_percentage": 85
    }

    result = predict_career(sample_user)

    print("Predicted Career:", result)