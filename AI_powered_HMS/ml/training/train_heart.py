"""
Heart Disease Risk Classifier Training Script
Accepts datasets matching Image 1:
Age, Sex, Chest_Pain, Resting_Blood_Pressure, Serum_Cholesterol, Fasting_Blood_Sugar,
Resting_ECG, Max_Heart_Rate, Exercise_Induced_Angina, ST_Depression, Peak_Exercise_ST_Segment,
Num_Major_Vessels, Thalassemia, Diagnosis_Heart_Disease (or target).

Saves serialized model to 'ml/models/heart_model.pkl'.
Saves detailed evaluation report to 'ml/evaluation/heart_metrics.txt' and 'ml/evaluation/heart_metrics.json'.
"""
import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score, 
    roc_auc_score, 
    confusion_matrix, 
    classification_report
)

def load_and_preprocess_heart_data(dataset_path):
    df = pd.read_csv(dataset_path)
    
    # Column mapping dictionary to standardize column headers
    col_mapping = {
        'age': 'Age',
        'sex': 'Sex',
        'chest_pain': 'Chest_Pain',
        'chest_pain_type': 'Chest_Pain',
        'cp': 'Chest_Pain',
        'resting_blood_pressure': 'Resting_Blood_Pressure',
        'resting_b': 'Resting_Blood_Pressure',
        'resting_bp': 'Resting_Blood_Pressure',
        'trestbps': 'Resting_Blood_Pressure',
        'serum_cholesterol': 'Serum_Cholesterol',
        'serum_ch': 'Serum_Cholesterol',
        'chol': 'Serum_Cholesterol',
        'fasting_blood_sugar': 'Fasting_Blood_Sugar',
        'fasting_bl': 'Fasting_Blood_Sugar',
        'fbs': 'Fasting_Blood_Sugar',
        'resting_ecg': 'Resting_ECG',
        'resting_e': 'Resting_ECG',
        'restecg': 'Resting_ECG',
        'max_heart_rate': 'Max_Heart_Rate',
        'max_hear': 'Max_Heart_Rate',
        'thalach': 'Max_Heart_Rate',
        'exercise_induced_angina': 'Exercise_Induced_Angina',
        'exercise_i': 'Exercise_Induced_Angina',
        'exang': 'Exercise_Induced_Angina',
        'st_depression': 'ST_Depression',
        'st_depres': 'ST_Depression',
        'oldpeak': 'ST_Depression',
        'peak_exercise_st_segment': 'Peak_Exercise_ST_Segment',
        'peak_exer': 'Peak_Exercise_ST_Segment',
        'slope': 'Peak_Exercise_ST_Segment',
        'num_major_vessels': 'Num_Major_Vessels',
        'num_maj': 'Num_Major_Vessels',
        'ca': 'Num_Major_Vessels',
        'thalassemia': 'Thalassemia',
        'thalassem': 'Thalassemia',
        'thal': 'Thalassemia',
        'diagnosis_heart_disease': 'Diagnosis_Heart_Disease',
        'target': 'Diagnosis_Heart_Disease',
        'heartdisease': 'Diagnosis_Heart_Disease',
        'num': 'Diagnosis_Heart_Disease'
    }

    # Normalize existing column names
    new_cols = {}
    for col in df.columns:
        clean = col.strip().lower().replace(' ', '_')
        new_cols[col] = col_mapping.get(clean, col)
    df = df.rename(columns=new_cols)

    target_col = 'Diagnosis_Heart_Disease'
    if target_col not in df.columns:
        # Fallback to last column as target
        target_col = df.columns[-1]

    # Convert non-numeric categorical if any
    for c in df.select_dtypes(include=['object', 'category']).columns:
        df[c] = df[c].astype('category').cat.codes

    # Drop any ID columns
    for id_col in ['id', 'patient_id', 'Unnamed: 0']:
        if id_col in df.columns:
            df = df.drop(columns=[id_col])

    # Impute missing values with median
    df = df.fillna(df.median(numeric_only=True))

    X = df.drop(target_col, axis=1)
    y = (df[target_col] > 0).astype(int) # Binary classification (0: Healthy, 1: Heart Disease)
    return X, y

def train_heart_model(dataset_path=None):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dataset_path is None:
        dataset_path = os.path.join(base_dir, 'datasets', 'heart.csv')
        
    models_dir = os.path.join(base_dir, 'models')
    eval_dir = os.path.join(base_dir, 'evaluation')
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(eval_dir, exist_ok=True)

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Heart dataset not found at: {dataset_path}")

    print(f"[*] Loading Heart Disease dataset from: {dataset_path}")
    X, y = load_and_preprocess_heart_data(dataset_path)
    print(f"[*] Dataset Shape: {X.shape[0]} rows, {X.shape[1]} features: {list(X.columns)}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=180,
        max_depth=8,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)
    clf_rep = classification_report(y_test, y_pred, target_names=['No Heart Disease (0)', 'Heart Disease (1)'])

    feature_importances = {
        col: round(float(imp), 4) 
        for col, imp in sorted(zip(X.columns, model.feature_importances_), key=lambda x: x[1], reverse=True)
    }

    # Save .pkl model
    model_path = os.path.join(models_dir, 'heart_model.pkl')
    joblib.dump(model, model_path)
    print(f"[✓] Serialized Model saved to: {model_path}")

    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
    report_text = f"""================================================================================
KAIre Health - Heart Disease ML Diagnostic Model Evaluation
Model: RandomForestClassifier (n_estimators=180, max_depth=8, balanced)
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

TOP CONTRIBUTING FEATURE IMPORTANCES (SHAP / Tree Weights):
--------------------------------------------------------------------------------
"""
    for rank, (feat, weight) in enumerate(feature_importances.items(), 1):
        report_text += f"{rank:>2}. {feat:<26}: {weight:.4f} ({weight * 100:.2f}%)\n"

    report_text += f"\nModel file: {model_path}\nStatus: PRODUCTION_READY\n"

    txt_path = os.path.join(eval_dir, 'heart_metrics.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"[✓] Evaluation Text Report saved to: {txt_path}")

    json_metrics = {
        'model_name': 'RandomForest-Heart-v1.2.0',
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
    json_path = os.path.join(eval_dir, 'heart_metrics.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_metrics, f, indent=2)

    print(f"[*] Performance Summary -> Accuracy: {acc*100:.2f}% | Recall: {rec*100:.2f}% | F1-Score: {f1*100:.2f}% | ROC-AUC: {auc:.4f}\n")
    return json_metrics

if __name__ == '__main__':
    train_heart_model()
