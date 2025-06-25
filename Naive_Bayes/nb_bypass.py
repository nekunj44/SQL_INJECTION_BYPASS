# nb_bypass.py

import pandas as pd
import random
import joblib
import urllib.parse
from sklearn.metrics import classification_report

# Load model and vectorizer
model = joblib.load("nb_model.pkl")
vectorizer = joblib.load("common_vectorizer.pkl")

# Load dataset (all queries, both 0 and 1 labels)
df = pd.read_csv("Modified_SQL_Dataset.csv")
df.dropna(inplace=True)
queries = df['Query'].astype(str).tolist()
true_labels = df['Label'].tolist()

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

def generate_super_adversarial(query):
    transformations = [
        homoglyph_replace,
        fragment_keywords,
        nested_url_encode,
        cloak_payload,
        inject_time_logic,
    ]
    transformed = query
    chosen = random.sample(transformations, 3)
    for func in chosen:
        transformed = func(transformed)
    return transformed

# Generate adversarial samples
super_adv_queries = [generate_super_adversarial(q) for q in queries]

# Predict
X_super = vectorizer.transform(super_adv_queries)
y_pred_super = model.predict(X_super)

# Calculate malicious bypasses
bypassed = sum(1 for true, pred in zip(true_labels, y_pred_super) if true == 1 and pred == 0)

# Report
print("\n💀 NB Model - Super Aggressive Adversarial Test Results (Full Dataset):\n")
print(f"⚠️  Summary: {bypassed} out of {true_labels.count(1)} malicious queries were BYPASSED after super-aggressive transformation.\n")

print("📊 Classification Report on All Adversarial Queries:")
print(classification_report(true_labels, y_pred_super))
