# SQL_INJECTION_BYPASS
# 🛡️ SQL Injection Detection using Machine Learning

Welcome to the **SQL Injection ML Detection** project! This repository showcases how machine learning can be leveraged to detect and classify SQL injection attacks based on query patterns. It includes model training, adversarial query generation, and bypass evaluations. 💡

---

## 📁 Project Structure

SQL_INJECTION_ML_BYPASS/
│
├── Modified_SQL_Dataset.csv # 🗂️ Dataset used for training/testing
├── common_vectorizer.pkl # 🔠 Shared TF-IDF vectorizer for all models
│
├── lr_model.py # 🤖 Train Logistic Regression
├── nb_model.py # 🤖 Train Naive Bayes
├── rf_model.py # 🤖 Train Random Forest
│
├── lr_bypass.py # 🔓 Adversarial testing for LR
├── nb_bypass.py # 🔓 Adversarial testing for NB
├── rf_bypass.py # 🔓 Adversarial testing for RF
│
├── *.pkl # 💾 Saved models
├── *.png # 📊 Visual results (optional)
└── vectorizer_setup.py # ⚙️ TF-IDF Vectorizer setup

---

## 🔍 Objective

To train and evaluate machine learning models for detecting SQL injection attacks and test their robustness using **super-aggressive adversarial techniques**.

---

## 🚀 Models Implemented

- ✅ **Logistic Regression**
- ✅ **Naive Bayes**
- ✅ **Random Forest**

All models are trained using TF-IDF vectorization and evaluated for:

- Accuracy
- Precision, Recall, F1-score
- Robustness against adversarial SQL injections

---

## 🧪 Adversarial Techniques Used

- 🔁 **Homoglyph Replacement**  
- 🧩 **Fragmented Keywords using SQL Comments**  
- 🌐 **Multi-layered URL Encoding**  
- 🎭 **Cloaking payloads in nested queries**  
- ⏳ **Time-based injections with `SLEEP()`**

Each bypass script randomly applies 3 transformations to generate super-aggressive queries.

---

## 📊 Sample Bypass Results

| Model               | Total Malicious Queries | Bypassed | 
|---------------------|-------------------------|----------|
| Logistic Regression | 11382                   | 6283     | 
| Naive Bayes         | 11382                   | 956      | 
| Random Forest       | 11382                   | 2714     | 

🧠 Key Insights
ML models can detect SQL injection patterns effectively.

However, they are vulnerable to obfuscation and bypass attacks.

Robust input sanitization + adversarial training is essential for production systems.

🧑‍💻 Author
Nekunj Khanna
🔗 LinkedIn
📁 GitHub

⭐ If you found this useful, give it a star!










