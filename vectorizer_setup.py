import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

df = pd.read_csv("Modified_SQL_Dataset.csv")
X = df['Query'].astype(str)

vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

joblib.dump(vectorizer, "common_vectorizer.pkl")
