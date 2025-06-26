# test_rf_bypass.py

import pandas as pd
import joblib
from sklearn.metrics import classification_report

# Load the trained Random Forest model and TF-IDF vectorizer
model = joblib.load("rf_model.pkl")
vectorizer = joblib.load("common_vectorizer.pkl")

# Load the same adversarial malicious queries used for other models
df = pd.read_csv("adversarial_malicious.csv")
X = vectorizer.transform(df["Query"].astype(str))
y_true = df["Label"].tolist()

# Predict using the RF model
y_pred = model.predict(X)

# Count how many malicious queries were bypassed
bypassed = sum(1 for pred in y_pred if pred == 0)
total = len(y_true)

# Print results
print("\n💀 Random Forest Model - Targeted Adversarial Bypass Test:\n")
print(f"⚠️  Summary: {bypassed} out of {total} malicious queries were BYPASSED.")
print(f"📉 Bypass Rate: {(bypassed / total) * 100:.2f}%\n")

print("📊 Classification Report (Malicious Only):")
print(classification_report(y_true, y_pred, labels=[1]))
