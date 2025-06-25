# rf_bypass_all.py

import pandas as pd
import random
import joblib
import urllib.parse
from sklearn.metrics import classification_report, confusion_matrix

# Load model and vectorizer
model = joblib.load("rf_model.pkl")
vectorizer = joblib.load("common_vectorizer.pkl")

# Load full dataset
df = pd.read_csv("Modified_SQL_Dataset.csv")
df.dropna(inplace=True)

# Use all queries and their true labels
all_queries = df['Query'].astype(str).tolist()
true_labels = df['Label'].tolist()

# Adversarial transformation functions
def homoglyph_replace(query):
    homoglyphs = {
        'O': 'Ο',  # Greek Omicron
        'a': 'а',  # Cyrillic a
        "'": '’',  # Right single quote
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

# Transform all queries
print("🔄 Applying super-aggressive transformations to all queries...")
super_adv_queries = [generate_super_adversarial(q) for q in all_queries]

# Vectorize and predict
X_super = vectorizer.transform(super_adv_queries)
y_pred_super = model.predict(X_super)

# Show results
print("\n💀 RF Model - Super Aggressive Adversarial Test Results:\n")
bypassed = 0
for i, (original, adv, pred, true) in enumerate(zip(all_queries, super_adv_queries, y_pred_super, true_labels)):
    if i < 10:  # Only print first 10 for readability
        print(f"Original Query    : {original}")
        print(f"Super Adversarial : {adv}")
        print(f"True Label        : {true}")
        print(f"Predicted Label   : {pred} ({'BYPASSED' if pred == 0 and true == 1 else 'OK'})")
        print("-" * 70)
    if pred == 0 and true == 1:
        bypassed += 1

print(f"\n⚠️  Summary: {bypassed} out of {true_labels.count(1)} malicious queries were BYPASSED after super-aggressive transformation.")

# Classification report
print("\n📊 Classification Report on All Adversarial Queries:")
print(classification_report(true_labels, y_pred_super))

# Optional: confusion matrix
#print("\n🧮 Confusion Matrix:")
#print(confusion_matrix(true_labels, y_pred_super))
