# test_nb_bypass.py
import pandas as pd
import joblib
from sklearn.metrics import classification_report

model = joblib.load("nb_model.pkl")
vectorizer = joblib.load("common_vectorizer.pkl")

df = pd.read_csv("adversarial_malicious.csv")
X = vectorizer.transform(df["Query"].astype(str))
y_true = df["Label"].tolist()
y_pred = model.predict(X)

bypassed = sum(1 for p in y_pred if p == 0)
print("\n💀 NB Model - Fixed Adversarial Bypass Test:\n")
print(f"⚠️  {bypassed} out of {len(y_true)} malicious queries were BYPASSED.")
print(f"📉 Bypass Rate: {(bypassed / len(y_true)) * 100:.2f}%\n")
print(classification_report(y_true, y_pred, labels=[1]))
