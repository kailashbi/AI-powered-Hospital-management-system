"""
Train all 3 ML models one by one and save .pkl + accuracy .txt to model/

Run from project root (inside venv):
    python train_all_models.py
"""
import os, sys, importlib.util

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)
sys.path.insert(0, BASE)


def run_script(path):
    spec   = importlib.util.spec_from_file_location("_train_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


# ── 1. Heart Disease  (Random Forest) ─────────────────────────────────────
run_script(os.path.join(BASE, "ml_pipeline", "train_heart_model.py"))

# ── 2. Diabetes  (Logistic Regression) ────────────────────────────────────
run_script(os.path.join(BASE, "ml_pipeline", "train_diabetes_model.py"))

# ── 3. Stroke  (XGBoost) ──────────────────────────────────────────────────
run_script(os.path.join(BASE, "ml_pipeline", "train_stroke_model.py"))


# ── Final summary ──────────────────────────────────────────────────────────
print("\n" + "="*55)
print("  ALL 3 MODELS TRAINED & SAVED SUCCESSFULLY!")
print()
model_dir = os.path.join(BASE, "model")
for fname in sorted(os.listdir(model_dir)):
    if fname == ".gitkeep":
        continue
    size = os.path.getsize(os.path.join(model_dir, fname))
    print(f"    ✔  {fname:<45}  ({size:,} bytes)")
print("="*55)
print("\n  Now run:  python app.py\n")