# test_lr_bypass.py

import pandas as pd
import joblib
from sklearn.metrics import classification_report

# Load the trained Logistic Regression model and vectorizer
model = joblib.load("sql_model.pkl")  # This is your LR model
vectorizer = joblib.load("common_vectorizer.pkl")

# Load the pre-generated adversarial queries
df = pd.read_csv("adversarial_malicious.csv")
X = vectorizer.transform(df["Query"].astype(str))
y_true = df["Label"].tolist()

# Predict using the loaded model
y_pred = model.predict(X)

# Count how many malicious queries were bypassed
bypassed = sum(1 for pred in y_pred if pred == 0)
total = len(y_true)

# Report
print("\n💀 Logistic Regression Model - Targeted Adversarial Bypass Test:\n")
print(f"⚠️  Summary: {bypassed} out of {total} malicious queries were BYPASSED.")
print(f"📉 Bypass Rate: {(bypassed / total) * 100:.2f}%\n")

print("📊 Classification Report (Malicious Only):")
print(classification_report(y_true, y_pred, labels=[1]))
