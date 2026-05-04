"""
CSC510 – Foundations of Artificial Intelligence
Portfolio Project – Final Submission
AI Alert Analyzer with NLP, Classification, Search, and FOL Reasoning

Author: Jessica Montgomery
Instructor: Dr. Gonzalez
Date: June 2, 2025

Description:
This program simulates an AI-powered alert analyzer for cloud operations. It uses natural language
processing (TF-IDF) and a logistic regression classifier to assess the severity of system alerts.
Alerts are prioritized using a Best-First Search heuristic based on severity, system criticality,
and urgency keywords. A symbolic expert system applies first-order logic rules to escalate,
suppress, or auto-close alerts.

Modules:
1. Data Loading and Preparation
2. NLP Vectorization and Classification
3. Best-First Search Prioritization
4. First-Order Logic-Based Decision System

Output:
- Confusion matrix and classification report for model evaluation
- Sample predictions on test alerts
- Ranked top 10 prioritized alerts
- CSV output with FOL-based decisions

"""


# Module 1: Load and Prepare Alert Data
import pandas as pd
import heapq
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from priority_engine import calculate_priority_score
from impact_engine import assess_impact
from risk_engine import simulate_risk

def recommend_action(severity, confidence, alert_text):
    severity = severity.lower()
    alert_lower = alert_text.lower()

    reason_flags = []

    if "production" in alert_lower or "prod" in alert_lower:
        reason_flags.append("production environment mentioned")

    if "authentication" in alert_lower or "access denied" in alert_lower:
        reason_flags.append("authentication or access issue detected")

    if "failed" in alert_lower or "error" in alert_lower:
        reason_flags.append("failure/error language detected")

    if severity == "critical":
        action = "Escalate immediately to on-call/cloud operations lead."
    elif severity == "high":
        action = "Investigate within the SLA window and correlate with related alerts."
    elif severity == "medium":
        action = "Monitor, correlate with related alerts, and review if repeated."
    else:
        action = "Suppress or log for trend analysis unless repeated."

    if confidence < 0.60:
        action += " Human review recommended due to low model confidence."

    reason = "Reason: " + "; ".join(reason_flags) if reason_flags else "Reason: Based on predicted severity and alert pattern."

    return action, reason

from decision_engine import recommend_action

# Step 1: Load Expanded Dataset
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "alert_dataset.csv")

df = pd.read_csv(data_path)

# Step 2: Preprocessing
X_text = df["message"]
y = df["historical_severity"]

# Module 2: NLP Feature Extraction and Classification
# Step 3: Vectorize Text
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(X_text)

# Step 4: Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Step 5: Train Classifier with Class Weight Balancing
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train, y_train)

# Step 6: Evaluate
y_pred = model.predict(X_test)
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

# Step 7: Predict on New Alerts
new_alerts = ["Disk usage at 95%", "Scheduled system backup", "Multiple failed login attempts"]
new_vectors = vectorizer.transform(new_alerts)
predictions = model.predict(new_vectors)

for msg, pred in zip(new_alerts, predictions):
    print(f"\n'{msg}' predicted as: {pred}")

# Decision engine output for sample alerts
print("\n📌 Decision Recommendation Examples:")

sample_alerts = [
    "Disk usage at 95%",
    "Scheduled system backup",
    "Multiple failed login attempts"
]

for alert_text in sample_alerts:
    predicted_severity = model.predict(vectorizer.transform([alert_text]))[0]
    probabilities = model.predict_proba(vectorizer.transform([alert_text]))
    confidence = probabilities.max()
    priority_score = calculate_priority_score(
            predicted_severity,
            confidence,
            alert_text
    )
    action, reason = recommend_action(predicted_severity, confidence, alert_text)
    impact = assess_impact(alert_text)
    risk = simulate_risk(alert_text, predicted_severity, impact)


    print(f"\nAlert: {alert_text}")
    print(f"Predicted Severity: {predicted_severity}")
    print(f"Confidence: {confidence:.2%}")
    print(f"Priority Score: {priority_score}")
    print(f"Recommended Action: {action}")
    print(reason)
    print(f"Impact Assessment: {impact}")
    print(f"Risk Simulation: {risk}")
# Define priority rules
severity_priority = {"critical": 0, "informational": 1, "false_positive": 2}
system_priority = {"database": 0, "backend": 0, "network": 0,
                   "frontend": 1, "email": 1, "storage": 1}
urgency_keywords = ["failed", "exceeds", "shutdown", "lost", "error", "latency", "delayed"]

# Heuristic scoring function
def compute_priority(alert_row, predicted_severity):
    sev_score = severity_priority.get(predicted_severity, 2)
    sys_score = system_priority.get(alert_row["system"], 1)
    msg = alert_row["message"].lower()
    keyword_bonus = -1 if any(word in msg for word in urgency_keywords) else 0
    return sev_score + sys_score + keyword_bonus

# Predict severity for all alerts
df["predicted_severity"] = model.predict(vectorizer.transform(df["message"]))

df["impact"] = df["message"].apply(assess_impact)

df["risk"] = df.apply(
    lambda row: simulate_risk(
        row["message"],
        row["predicted_severity"],
        row["impact"]
    ),
    axis=1
)

df["intelligent_priority_score"] = df.apply(
    lambda row: calculate_priority_score(
        row["predicted_severity"],
        0.75,
        row["message"]
    ),
    axis=1
)

df_sorted = df.sort_values(by="intelligent_priority_score", ascending=False)

print("\n📋 Top 10 Alerts with Intelligent Priority Scoring:")
print(df_sorted[["message", "system", "predicted_severity", "intelligent_priority_score", "impact", "risk"]].head(10))
# Create aectorizer.transform(df["message"])
# Create priority queue
# Predict severity for all alerts


# Module 4: First-Order Logic (FOL) Rules 
def apply_fol_rules(alert):
    severity = alert["predicted_severity"]
    system = alert["system"].lower()
    message = alert["message"].lower()

    if severity == "critical" and system in ["database", "backend"]:
        return "ESCALATE: Notify on-call engineer"
    elif severity == "informational" and any(word in message for word in ["maintenance", "backup"]):
        return "SUPPRESS: Routine informational"
    elif severity == "false_positive":
        return "AUTO-CLOSE: No action needed"
    else:
        return "REVIEW: Manual inspection required"

# Apply FOL rules to all alerts
df["FOL_decision"] = df.apply(apply_fol_rules, axis=1)
df["intelligent_priority_score"] = df.apply(
    lambda row: calculate_priority_score(
        row["predicted_severity"],
        0.75,
        row["message"]
    ),
    axis=1
)


# Save final results
df_sorted.head(10).to_csv("top_10_with_intelligent_priority.csv", index=False)

# Preview output
