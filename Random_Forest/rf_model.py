# rf_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Load Dataset
df = pd.read_csv("Modified_SQL_Dataset.csv")
df.dropna(inplace=True)

# Feature and Label
X = df['Query'].astype(str)
y = df['Label']

# TF-IDF Vectorization
vectorizer = joblib.load("common_vectorizer.pkl")
X_vectorized = vectorizer.transform(df['Query'].astype(str))

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)

# Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("\n✅ Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\n✅ Classification Report:")
print(classification_report(y_test, y_pred))

# Save model and vectorizer
joblib.dump(model, "rf_model.pkl")
joblib.dump(vectorizer, "common_vectorizer.pkl")
