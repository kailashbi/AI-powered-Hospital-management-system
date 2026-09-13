"""
Type-2 Diabetes Risk Classifier Training Script (Logistic Regression)
Accepts datasets matching Image 2:
gender, age, hypertension, heart_disease, smoking_history, bmi, hbA1c_level, blood_glucose_level, diabetes.
Also supports optional demographic columns (location, race:*, year) and standard Pima formats.

Uses LogisticRegression with StandardScaler and balanced class weights.
Saves serialized model to 'ml/models/diabetes_model.pkl' and scaler to 'ml/models/diabetes_scaler.pkl'.
Saves detailed evaluation report to 'ml/evaluation/diabetes_metrics.txt' and 'ml/evaluation/diabetes_metrics.json'.
"""
import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score, 
    roc_auc_score, 
    confusion_matrix, 
    classification_report
)

def load_and_preprocess_diabetes_data(dataset_path):
    df = pd.read_csv(dataset_path)
    
    clean_cols = {c: c.strip().lower() for c in df.columns}
    df = df.rename(columns=clean_cols)

    # Determine target column
    target_col = None
    for cand in ['diabetes', 'outcome', 'target', 'class']:
        if cand in df.columns:
            target_col = cand
            break
    if not target_col:
        target_col = df.columns[-1]

    # Drop non-predictive metadata columns if present
    for drop_cand in ['year', 'location', 'id', 'patient_id', 'unnamed: 0']:
        if drop_cand in df.columns:
            df = df.drop(columns=[drop_cand])

    # Convert categorical strings to numeric codes
    if 'gender' in df.columns and df['gender'].dtype == object:
        df['gender'] = df['gender'].map({'Male': 1, 'Female': 0, 'Other': 0}).fillna(0)
        
    if 'smoking_history' in df.columns and df['smoking_history'].dtype == object:
        smoke_map = {'never': 0, 'No Info': 0, 'not current': 1, 'former': 2, 'formerly': 2, 'current': 3, 'ever': 2}
        df['smoking_history'] = df['smoking_history'].map(smoke_map).fillna(0)

    # Handle any other categorical columns (e.g. race columns)
    for col in df.select_dtypes(include=['object', 'category']).columns:
        df[col] = df[col].astype('category').cat.codes

    # Fill missing values with median
    df = df.fillna(df.median(numeric_only=True))

    X = df.drop(target_col, axis=1)
    y = df[target_col].astype(int)
    return X, y

def train_diabetes_model(dataset_path=None):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dataset_path is None:
        dataset_path = os.path.join(base_dir, 'datasets', 'diabetes.csv')

    models_dir = os.path.join(base_dir, 'models')
    eval_dir = os.path.join(base_dir, 'evaluation')
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(eval_dir, exist_ok=True)

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Diabetes dataset not found at: {dataset_path}")

    print(f"[*] Loading Diabetes dataset from: {dataset_path}")
    X, y = load_and_preprocess_diabetes_data(dataset_path)
    print(f"[*] Dataset Shape: {X.shape[0]} rows, {X.shape[1]} features: {list(X.columns)}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Standard Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Model: Logistic Regression
    model = LogisticRegression(
        max_iter=1000,
        C=1.0,
        class_weight='balanced',
        solver='lbfgs',
        random_state=42
    )
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)
    clf_rep = classification_report(y_test, y_pred, target_names=['Non-Diabetic (0)', 'Diabetic (1)'])

    # Feature Importance from Logistic Regression Coefficients (abs weight)
    coefs = model.coef_[0]
    total_abs = sum(abs(c) for c in coefs) if sum(abs(c) for c in coefs) > 0 else 1.0
    feature_importances = {
        col: round(float(abs(c) / total_abs), 4)
        for col, c in sorted(zip(X.columns, coefs), key=lambda x: abs(x[1]), reverse=True)
    }

    # Save .pkl model and scaler
    model_path = os.path.join(models_dir, 'diabetes_model.pkl')
    scaler_path = os.path.join(models_dir, 'diabetes_scaler.pkl')
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"[✓] Serialized Logistic Regression Model saved to: {model_path}")
    print(f"[✓] Serialized Scaler saved to: {scaler_path}")

    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
    report_text = f"""================================================================================
KAIre Health - Type-2 Diabetes ML Diagnostic Model Evaluation
Model: LogisticRegression (StandardScaler + Balanced Weights, max_iter=1000)
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

LOGISTIC REGRESSION FEATURE IMPORTANCES (Normalized Log-Odds Weights):
--------------------------------------------------------------------------------
"""
    for rank, (feat, weight) in enumerate(feature_importances.items(), 1):
        report_text += f"{rank:>2}. {feat:<26}: {weight:.4f} ({weight * 100:.2f}%)\n"

    report_text += f"\nModel file: {model_path}\nScaler file: {scaler_path}\nStatus: PRODUCTION_READY\n"

    txt_path = os.path.join(eval_dir, 'diabetes_metrics.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"[✓] Evaluation Text Report saved to: {txt_path}")

    json_metrics = {
        'model_name': 'LogisticRegression-Diabetes-v1.0.4',
        'dataset': os.path.basename(dataset_path),
        'total_samples': int(len(X)),
        'accuracy': round(float(acc), 4),
        'precision': round(float(prec), 4),
        'recall': round(float(rec), 4),
        'f1_score': round(float(f1), 4),
        'roc_auc': round(float(auc), 4),
        'confusion_matrix': {'tn': int(tn), 'fp': int(fp), 'fn': int(fn), 'tp': int(tp)},
        'features': list(X.columns),
        'feature_importances': feature_importances
    }
    json_path = os.path.join(eval_dir, 'diabetes_metrics.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_metrics, f, indent=2)

    print(f"[*] Performance Summary -> Accuracy: {acc*100:.2f}% | Recall: {rec*100:.2f}% | F1-Score: {f1*100:.2f}% | ROC-AUC: {auc:.4f}\n")
    return json_metrics

if __name__ == '__main__':
    train_diabetes_model()
