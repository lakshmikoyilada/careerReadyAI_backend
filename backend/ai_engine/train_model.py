import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score

from scipy.sparse import hstack


# =========================
# LOAD DATASET
# =========================

data = pd.read_csv("datasets/career_dataset.csv")

print("Dataset Loaded Successfully")
print(data.head())


# =========================
# REMOVE NULL VALUES
# =========================

data = data.dropna()


# =========================
# COMBINE TEXT FEATURES
# =========================

data["combined_text"] = (
    data["Education Level"].astype(str) + " " +
    data["Specialization"].astype(str) + " " +
    data["Skills"].astype(str) + " " +
    data["Certifications"].astype(str)
)


# =========================
# TF-IDF VECTORIZATION
# =========================

tfidf = TfidfVectorizer()

X_text = tfidf.fit_transform(data["combined_text"])


# =========================
# ADD CGPA FEATURE
# =========================

X_numeric = data[["CGPA/Percentage"]].values


# =========================
# COMBINE FEATURES
# =========================

X = hstack([X_text, X_numeric])


# =========================
# TARGET OUTPUT
# =========================

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(data["Recommended Career"])


# =========================
# SPLIT DATA
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# =========================
# TRAIN MODEL
# =========================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)


# =========================
# TEST MODEL
# =========================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy * 100:.2f}%")


# =========================
# SAVE MODEL
# =========================

joblib.dump(model, "models/career_model.pkl")

joblib.dump(label_encoder, "models/label_encoder.pkl")

joblib.dump(tfidf, "models/tfidf_vectorizer.pkl")

print("Model saved successfully")