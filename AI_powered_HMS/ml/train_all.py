"""
KAIre Health - Master ML Training & Evaluation Runner
Trains all 3 clinical diagnostic models:
1. Heart Disease: RandomForestClassifier
2. Type-2 Diabetes: LogisticRegression (StandardScaler + Balanced Weights)
3. Stroke Risk: XGBClassifier (XGBoost Pipeline + OneHotEncoder)

Serializes validated models as .pkl artifacts, and saves comprehensive accuracy, precision,
recall, and F1-score performance reports to .txt and .json files.
"""
import os
import sys
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.training.train_heart import train_heart_model
from ml.training.train_diabetes import train_diabetes_model
from ml.training.train_stroke import train_stroke_model

def run_ml_pipeline():
    start_time = time.time()
    base_dir = os.path.abspath(os.path.dirname(__file__))
    eval_dir = os.path.join(base_dir, 'evaluation')
    datasets_dir = os.path.join(base_dir, 'datasets')
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(eval_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(datasets_dir, exist_ok=True)

    print("=" * 80)
    print("🏥 KAIre Health - Automated Clinical ML Training & Model Validation Pipeline")
    print("=" * 80)

    # 1. Verify / Generate Benchmark Datasets if missing
    heart_csv = os.path.join(datasets_dir, 'heart.csv')
    diabetes_csv = os.path.join(datasets_dir, 'diabetes.csv')
    stroke_csv = os.path.join(datasets_dir, 'stroke.csv')
    
    if not (os.path.exists(heart_csv) and os.path.exists(diabetes_csv) and os.path.exists(stroke_csv)):
        print("\n[*] Initializing clinical benchmark datasets from generate_datasets.py...")
        try:
            import subprocess
            subprocess.run([sys.executable, os.path.join(base_dir, 'generate_datasets.py')], check=True)
        except Exception:
            pass

    # 2. Train Model 1: Heart Disease (Random Forest)
    print("\n" + "-" * 80)
    print("🫀 [1/3] Training Heart Disease Risk Classifier (Random Forest)...")
    print("-" * 80)
    heart_metrics = train_heart_model()

    # 3. Train Model 2: Type-2 Diabetes (Logistic Regression)
    print("\n" + "-" * 80)
    print("🩸 [2/3] Training Type-2 Diabetes Predictor (Logistic Regression + Scaler)...")
    print("-" * 80)
    diabetes_metrics = train_diabetes_model()

    # 4. Train Model 3: Stroke Risk (XGBoost)
    print("\n" + "-" * 80)
    print("🧠 [3/3] Training Stroke Risk Stratifier (XGBoost Pipeline + OHE)...")
    print("-" * 80)
    stroke_metrics = train_stroke_model()

    # 5. Generate Master Evaluation Summary TXT Report
    elapsed = time.time() - start_time
    summary_text = f"""================================================================================
🏥 KAIre Health - Master Clinical ML Models Benchmark Summary
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}
Total Training & Evaluation Duration: {elapsed:.2f} seconds
================================================================================

PERFORMANCE BENCHMARK SUMMARY TABLE:
--------------------------------------------------------------------------------
Disease Model                      | Accuracy | Precision | Recall   | F1-Score | ROC-AUC
--------------------------------------------------------------------------------
Heart Disease (Random Forest)      | {heart_metrics['accuracy']*100:>7.2f}% | {heart_metrics['precision']*100:>8.2f}% | {heart_metrics['recall']*100:>7.2f}% | {heart_metrics['f1_score']*100:>7.2f}% | {heart_metrics['roc_auc']:>7.4f}
Type-2 Diabetes (Logistic Reg.)    | {diabetes_metrics['accuracy']*100:>7.2f}% | {diabetes_metrics['precision']*100:>8.2f}% | {diabetes_metrics['recall']*100:>7.2f}% | {diabetes_metrics['f1_score']*100:>7.2f}% | {diabetes_metrics['roc_auc']:>7.4f}
Stroke Risk (XGBoost Pipeline)     | {stroke_metrics['accuracy']*100:>7.2f}% | {stroke_metrics['precision']*100:>8.2f}% | {stroke_metrics['recall']*100:>7.2f}% | {stroke_metrics['f1_score']*100:>7.2f}% | {stroke_metrics['roc_auc']:>7.4f}
--------------------------------------------------------------------------------

GENERATED SERIALIZED MODEL ARTIFACTS:
- ml/models/heart_model.pkl (RandomForestClassifier)
- ml/models/diabetes_model.pkl (LogisticRegression)
- ml/models/diabetes_scaler.pkl (StandardScaler)
- ml/models/stroke_model.pkl (XGBoost Pipeline)

GENERATED TEXT METRIC EVALUATION REPORTS:
- ml/evaluation/heart_metrics.txt
- ml/evaluation/diabetes_metrics.txt
- ml/evaluation/stroke_metrics.txt
- ml/evaluation/all_models_summary.txt
================================================================================
"""

    summary_file = os.path.join(eval_dir, 'all_models_summary.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_text)

    print("\n" + "=" * 80)
    print(summary_text)
    print(f"[✓] Master Evaluation Summary saved to: {summary_file}")
    print("[✓] All 3 models trained and ready for live clinical inference!\n")

if __name__ == '__main__':
    run_ml_pipeline()
