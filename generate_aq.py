import pandas as pd
import random
import urllib.parse

# Load data
df = pd.read_csv("Modified_SQL_Dataset.csv")
malicious_df = df[df['Label'] == 1]
queries = malicious_df['Query'].astype(str).tolist()

# Adversarial transforms
def homoglyph_replace(query):
    homoglyphs = {'O': 'Ο', 'a': 'а', "'": '’'}
    return ''.join(homoglyphs.get(c, c) for c in query)

def fragment_keywords(query):
    replacements = {
        "SELECT": "SE/**/LECT", "UNION": "UN/**/ION", "WHERE": "W/**/HERE",
        "FROM": "FR/**/OM", "AND": "A/**/ND", "OR": "O/**/R"
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
    transformations = [homoglyph_replace, fragment_keywords, nested_url_encode, cloak_payload, inject_time_logic]
    transformed = query
    chosen = random.sample(transformations, 3)
    for func in chosen:
        transformed = func(transformed)
    return transformed

# Set seed once to keep output fixed
random.seed(42)
adversarial_queries = [generate_super_adversarial(q) for q in queries]

# Save once
pd.DataFrame({"Query": adversarial_queries, "Label": 1}).to_csv("adversarial_malicious.csv", index=False)
print("✅ Adversarial malicious queries saved to 'adversarial_malicious.csv'")
