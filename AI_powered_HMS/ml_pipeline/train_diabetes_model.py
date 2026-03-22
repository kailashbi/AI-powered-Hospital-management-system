"""
Diabetes Model — Logistic Regression
Dataset columns: Pregnancies, Glucose, BloodPressure, SkinThickness,
                 Insulin, BMI, DiabetesPedigreeFunction, Age, Outcome
Target column  : Outcome  (0=No Diabetes, 1=Diabetes)
"""
import os, pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

BASE      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

print("\n" + "="*55)
print("  DIABETES MODEL  —  Logistic Regression")
print("="*55)

data = pd.read_csv(os.path.join(BASE, "dataset", "diabetes.csv"))
print(f"  Dataset  : {data.shape[0]} rows x {data.shape[1]} columns")
print(f"  Columns  : {data.columns.tolist()}")

# ── Fill any NaN ──────────────────────────────────────────────────────────
data = data.fillna(data.median(numeric_only=True))

X = data.drop("Outcome", axis=1)
y = data["Outcome"]
print(f"  Features : {X.shape[1]}  |  Target: 'Outcome'  |  Classes: {sorted(y.unique().tolist())}")

scaler   = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc    = accuracy_score(y_test, y_pred)

print(f"  Accuracy : {acc*100:.2f}%")
report = classification_report(y_test, y_pred, target_names=["No Diabetes", "Diabetes"])
print(f"\n{report}")

with open(os.path.join(MODEL_DIR, "diabetes_model_accuracy.txt"), "w") as f:
    f.write("Diabetes Model — Logistic Regression\n")
    f.write(f"Accuracy : {acc*100:.2f}%\n\n")
    f.write(report)

joblib.dump(model,  os.path.join(MODEL_DIR, "diabetes_model.pkl"))
joblib.dump(scaler, os.path.join(MODEL_DIR, "diabetes_scaler.pkl"))

print(f"  Saved → model/diabetes_model.pkl")
print(f"  Saved → model/diabetes_scaler.pkl")
print(f"  Saved → model/diabetes_model_accuracy.txt")