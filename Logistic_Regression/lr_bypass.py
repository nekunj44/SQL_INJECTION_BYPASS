import pandas as pd
import random
import joblib
import urllib.parse
from sklearn.metrics import classification_report

# Load model and vectorizer
model = joblib.load("sql_model.pkl")  # Logistic Regression model
vectorizer = joblib.load("common_vectorizer.pkl")

# Load dataset
df = pd.read_csv("Modified_SQL_Dataset.csv")
df.dropna(inplace=True)
queries = df['Query'].astype(str).tolist()
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

# Generate adversarial examples for all queries
super_adv_queries = [generate_super_adversarial(q) for q in queries]

# Vectorize and predict
X_super = vectorizer.transform(super_adv_queries)
y_pred_super = model.predict(X_super)

# Calculate bypasses for Label=1 (malicious)
bypassed = 0
total_malicious = 0
for true, pred in zip(true_labels, y_pred_super):
    if true == 1:
        total_malicious += 1
        if pred == 0:
            bypassed += 1

# Print results
print("\n💀 Logistic Regression Model - Super Aggressive Adversarial Test Results:\n")
print(f"⚠️  Summary: {bypassed} out of {total_malicious} malicious queries were BYPASSED after super-aggressive transformation.\n")

print("📊 Classification Report on All Adversarial Queries:")
print(classification_report(true_labels, y_pred_super))
