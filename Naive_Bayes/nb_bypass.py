# nb_bypass_malicious_only.py

import pandas as pd
import random
import joblib
import urllib.parse
from sklearn.metrics import classification_report

# Load model and vectorizer
model = joblib.load("nb_model.pkl")
vectorizer = joblib.load("common_vectorizer.pkl")

# Load dataset (only malicious queries)
df = pd.read_csv("Modified_SQL_Dataset.csv")
df.dropna(inplace=True)

malicious_df = df[df['Label'] == 1]
malicious_queries = malicious_df['Query'].astype(str).tolist()
true_labels = [1] * len(malicious_queries)  # All are malicious

# Adversarial transformation functions
def homoglyph_replace(query):
    homoglyphs = {
        'O': 'Ο',
        'a': 'а',
        "'": '’',
    }
    return ''.join(homoglyphs.get(c, c) for c in query)

def fragment_keywords(query):
    replacements = {
        "SELECT": "SE/**/LECT",
        "UNION": "UN/**/ION",
        "WHERE": "W/**/HERE",
        "FROM": "FR/**/OM",
        "AND": "A/**/ND",
        "OR": "O/**/R"
    }
    for k, v in replacements.items():
        query = query.replace(k, v).replace(k.lower(), v.lower())
    return query

def nested_url_encode(query, layers=2):
    for _ in range(layers):
        query = urllib.parse.quote(query)
    return query

def cloak_payload(query):
    return f"SELECT * FROM (SELECT '{query}') AS benign_sub"

def inject_time_logic(query):
    return f"IF(1=1, SLEEP(5), 0)--{query}"

# Apply 3 random transformations
def generate_super_adversarial(query):
    transformations = [
        homoglyph_replace,
        fragment_keywords,
        nested_url_encode,
        cloak_payload,
        inject_time_logic,
    ]
    chosen = random.sample(transformations, 3)
    transformed = query
    for func in chosen:
        transformed = func(transformed)
    return transformed

# Reproducibility
random.seed(42)

# Generate adversarial queries for malicious ones
super_adv_queries = [generate_super_adversarial(q) for q in malicious_queries]

# Predict
X_super = vectorizer.transform(super_adv_queries)
y_pred_super = model.predict(X_super)

# Count bypasses
bypassed = sum(1 for pred in y_pred_super if pred == 0)
total = len(true_labels)

# Print results
print("\n💀 Naive Bayes Model - Targeted Adversarial Bypass Test:\n")
print(f"⚠️  Summary: {bypassed} out of {total} malicious queries were BYPASSED.")
print(f"📉 Bypass Rate: {(bypassed / total) * 100:.2f}%\n")

print("📊 Classification Report (Malicious Only):")
print(classification_report(true_labels, y_pred_super, labels=[1]))
