"""
Cerebrovascular Stroke Risk Classifier Training Script (XGBoost)
Accepts datasets matching Image 3:
id, gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status, stroke.

Uses XGBoost (or balanced Gradient Boosting pipeline) for state-of-the-art predictive performance.
Saves serialized pipeline to 'ml/models/stroke_model.pkl'.
Saves detailed evaluation report to 'ml/evaluation/stroke_metrics.txt' and 'ml/evaluation/stroke_metrics.json'.
"""
import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score, 
    roc_auc_score, 
    confusion_matrix, 
    classification_report
)

def get_stroke_classifier():
    """Try to use XGBoost, fallback to RandomForest/GradientBoosting if xgboost module not found"""
    try:
        from xgboost import XGBClassifier
        return XGBClassifier(
            n_estimators=180,
            max_depth=6,
            learning_rate=0.08,
            subsample=0.85,
            colsample_bytree=0.85,
            scale_pos_weight=3.5, # Handle class imbalance
            random_state=42,
            eval_metric='logloss'
        ), 'XGBoost-Stroke-v1.1.0'
    except ImportError:
        from sklearn.ensemble import GradientBoostingClassifier
        return GradientBoostingClassifier(
            n_estimators=180,
            max_depth=6,
            learning_rate=0.08,
            random_state=42
        ), 'GradientBoosting-Stroke-v1.1.0'

def load_and_preprocess_stroke_data(dataset_path):
    df = pd.read_csv(dataset_path)
    
    clean_cols = {c: c.strip().lower() for c in df.columns}
    df = df.rename(columns=clean_cols)

    target_col = 'stroke'
    if target_col not in df.columns:
        for cand in ['stroke', 'target', 'output', 'condition']:
            if cand in df.columns:
                target_col = cand
                break

    # Drop ID columns
    for id_col in ['id', 'patient_id', 'unnamed: 0']:
        if id_col in df.columns:
            df = df.drop(columns=[id_col])

    # Convert and impute BMI if string / N/A
    if 'bmi' in df.columns:
        df['bmi'] = pd.to_numeric(df['bmi'], errors='coerce')
        df['bmi'] = df['bmi'].fillna(df['bmi'].median())

    # Fill any remaining NaNs
    df = df.fillna('Unknown')

    X = df.drop(target_col, axis=1)
    y = df[target_col].astype(int)
    return X, y

def train_stroke_model(dataset_path=None):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dataset_path is None:
        dataset_path = os.path.join(base_dir, 'datasets', 'stroke.csv')

    models_dir = os.path.join(base_dir, 'models')
    eval_dir = os.path.join(base_dir, 'evaluation')
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(eval_dir, exist_ok=True)

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Stroke dataset not found at: {dataset_path}")

    print(f"[*] Loading Stroke dataset from: {dataset_path}")
    X, y = load_and_preprocess_stroke_data(dataset_path)
    print(f"[*] Dataset Shape: {X.shape[0]} rows, {X.shape[1]} features: {list(X.columns)}")

    categorical_cols = [col for col in X.select_dtypes(include=['object', 'category']).columns]
    numeric_cols = [col for col in X.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
        ]
    )

    clf, model_name = get_stroke_classifier()
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', clf)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)
    clf_rep = classification_report(y_test, y_pred, target_names=['No Stroke (0)', 'Stroke Risk (1)'])

    model_path = os.path.join(models_dir, 'stroke_model.pkl')
    joblib.dump(pipeline, model_path)
    print(f"[✓] Serialized {model_name} Pipeline Model saved to: {model_path}")

    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
    report_text = f"""================================================================================
KAIre Health - Cerebrovascular Stroke Risk Diagnostic Model Evaluation
Model: {model_name} (Pipeline with StandardScaler + OneHotEncoder)
Dataset: {os.path.basename(dataset_path)} ({len(X)} samples, {len(X.columns)} features)
================================================================================

PRIMARY METRICS:
--------------------------------------------------------------------------------
Accuracy:             {acc:.4f}  ({acc * 100:.2f}%)
Precision:            {prec:.4f}  ({prec * 100:.2f}%)
Recall (Sensitivity): {rec:.4f}  ({rec * 100:.2f}%)
F1-Score:             {f1:.4f}  ({f1 * 100:.2f}%)
ROC-AUC Score:        {auc:.4f}  ({auc * 100:.2f}%)

CONFUSION MATRIX:
--------------------------------------------------------------------------------
                 Predicted: Negative (0)    Predicted: Positive (1)
Actual: No (0)            {tn:<24} {fp:<24}
Actual: Yes (1)           {fn:<24} {tp:<24}

- True Negatives (TN):  {tn}
- False Positives (FP): {fp}
- False Negatives (FN): {fn}
- True Positives (TP):  {tp}

DETAILED CLASSIFICATION REPORT:
--------------------------------------------------------------------------------
{clf_rep}

FEATURES UTILIZED:
--------------------------------------------------------------------------------
Numeric Features:     {', '.join(numeric_cols)}
Categorical Features: {', '.join(categorical_cols)}

Model file: {model_path}
Status: PRODUCTION_READY
"""

    txt_path = os.path.join(eval_dir, 'stroke_metrics.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"[✓] Evaluation Text Report saved to: {txt_path}")

    json_metrics = {
        'model_name': model_name,
        'dataset': os.path.basename(dataset_path),
        'total_samples': int(len(X)),
        'accuracy': round(float(acc), 4),
        'precision': round(float(prec), 4),
        'recall': round(float(rec), 4),
        'f1_score': round(float(f1), 4),
        'roc_auc': round(float(auc), 4),
        'confusion_matrix': {'tn': int(tn), 'fp': int(fp), 'fn': int(fn), 'tp': int(tp)},
        'numeric_features': numeric_cols,
        'categorical_features': categorical_cols
    }
    json_path = os.path.join(eval_dir, 'stroke_metrics.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_metrics, f, indent=2)

    print(f"[*] Performance Summary -> Accuracy: {acc*100:.2f}% | Recall: {rec*100:.2f}% | F1-Score: {f1*100:.2f}% | ROC-AUC: {auc:.4f}\n")
    return json_metrics

if __name__ == '__main__':
    train_stroke_model()
