"""
Stroke Model — XGBoost Classifier
Dataset columns: id, gender, age, hypertension, heart_disease, ever_married,
                 work_type, Residence_type, avg_glucose, bmi, smoking_status, stroke
Target column  : stroke  (0=No Stroke, 1=Stroke)
"""
import os, pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

BASE      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

print("\n" + "="*55)
print("  STROKE MODEL  —  XGBoost Classifier")
print("="*55)

data = pd.read_csv(os.path.join(BASE, "dataset", "stroke.csv"))
print(f"  Dataset  : {data.shape[0]} rows x {data.shape[1]} columns")
print(f"  Columns  : {data.columns.tolist()}")

# ── Drop id column ────────────────────────────────────────────────────────
if "id" in data.columns:
    data = data.drop("id", axis=1)

# ── Handle bmi: 'N/A' string + actual NaN both replaced with median ───────
data["bmi"] = pd.to_numeric(data["bmi"], errors="coerce")
data["bmi"] = data["bmi"].fillna(data["bmi"].median())

# ── Label-encode all categorical columns ─────────────────────────────────
categorical_cols = ["gender", "ever_married", "work_type", "Residence_type", "smoking_status"]
le = LabelEncoder()
for col in categorical_cols:
    if col in data.columns:
        data[col] = le.fit_transform(data[col].astype(str))

X = data.drop("stroke", axis=1)
y = data["stroke"]
print(f"  Features : {X.shape[1]}  |  Target: 'stroke'  |  Classes: {sorted(y.unique().tolist())}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = XGBClassifier(
    n_estimators=200, learning_rate=0.05,
    max_depth=6, eval_metric="logloss",
    random_state=42, use_label_encoder=False
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc    = accuracy_score(y_test, y_pred)

print(f"  Accuracy : {acc*100:.2f}%")
report = classification_report(y_test, y_pred, target_names=["No Stroke", "Stroke"])
print(f"\n{report}")

with open(os.path.join(MODEL_DIR, "stroke_model_accuracy.txt"), "w") as f:
    f.write("Stroke Model — XGBoost Classifier\n")
    f.write(f"Accuracy : {acc*100:.2f}%\n\n")
    f.write(report)

joblib.dump(model, os.path.join(MODEL_DIR, "stroke_model.pkl"))

print(f"  Saved → model/stroke_model.pkl")
print(f"  Saved → model/stroke_model_accuracy.txt")