"""
Heart Disease Model — Random Forest Classifier
Dataset columns: id, age, sex, dataset, cp, trestbps, chol, fbs, restecg,
                 thalch, exang, oldpeak, slope, ca, thal, num
Target column  : num  (0 = No Disease, 1/2/3/4 = Disease → binarised to 0/1)
"""
import os, pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

BASE      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

print("\n" + "="*55)
print("  HEART DISEASE MODEL  —  Random Forest Classifier")
print("="*55)

data = pd.read_csv(os.path.join(BASE, "dataset", "heart.csv"))
print(f"  Dataset  : {data.shape[0]} rows x {data.shape[1]} columns")
print(f"  Columns  : {data.columns.tolist()}")

# ── Drop non-feature columns ──────────────────────────────────────────────
drop_cols = [c for c in ["id", "dataset"] if c in data.columns]
if drop_cols:
    data = data.drop(drop_cols, axis=1)

# ── Target column is 'num' (0=healthy, >0=disease) → binarise ────────────
data["num"] = (data["num"] > 0).astype(int)

# ── Handle categorical columns (sex, cp, fbs, restecg, exang, slope, thal)
cat_cols = data.select_dtypes(include=["object", "bool"]).columns.tolist()
if cat_cols:
    print(f"  Encoding : {cat_cols}")
    data = pd.get_dummies(data, columns=cat_cols, drop_first=True)

# ── Fill any remaining NaN ────────────────────────────────────────────────
data = data.fillna(data.median(numeric_only=True))

X = data.drop("num", axis=1)
y = data["num"]
print(f"  Features : {X.shape[1]}  |  Target: 'num'  |  Classes: {sorted(y.unique().tolist())}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc    = accuracy_score(y_test, y_pred)

print(f"  Accuracy : {acc*100:.2f}%")
report = classification_report(y_test, y_pred, target_names=["No Disease", "Heart Disease"])
print(f"\n{report}")

# ── Save accuracy report ──────────────────────────────────────────────────
with open(os.path.join(MODEL_DIR, "heart_model_accuracy.txt"), "w") as f:
    f.write("Heart Disease Model — Random Forest Classifier\n")
    f.write(f"Accuracy : {acc*100:.2f}%\n\n")
    f.write(report)

# ── Save model + feature list (needed by predict.py) ─────────────────────
joblib.dump(model,            os.path.join(MODEL_DIR, "heart_model.pkl"))
joblib.dump(X.columns.tolist(), os.path.join(MODEL_DIR, "heart_features.pkl"))

print(f"  Saved → model/heart_model.pkl")
print(f"  Saved → model/heart_features.pkl")
print(f"  Saved → model/heart_model_accuracy.txt")