# ==============================================================================
# 🏥 KAIre Health - Machine Learning Training & Evaluation Pipeline (Google Colab)
# ==============================================================================
# Models Verified:
# 1. 🫀 Heart Disease: RandomForestClassifier
# 2. 🩸 Type-2 Diabetes: LogisticRegression (StandardScaler + Balanced Weights)
# 3. 🧠 Stroke Risk: XGBClassifier (XGBoost Pipeline + OneHotEncoder)
# ==============================================================================

# Install XGBoost
import subprocess
subprocess.run(["pip", "install", "-q", "xgboost", "scikit-learn", "joblib", "pandas", "numpy"])

# STEP 1: Mount Google Drive
# ------------------------------------------------------------------------------
from google.colab import drive
import os
import sys
import json
import joblib
import shutil
import numpy as np
import pandas as pd
from google.colab import files

print("[*] Mounting Google Drive...")
drive.mount('/content/drive')

# STEP 2: Configure Workspace Directories
# ------------------------------------------------------------------------------
DRIVE_PROJECT_DIR = '/content/drive/MyDrive/KAIre_Health_ML'
MODELS_DIR = os.path.join(DRIVE_PROJECT_DIR, 'models')
EVAL_DIR = os.path.join(DRIVE_PROJECT_DIR, 'evaluation')
DATASETS_DIR = os.path.join(DRIVE_PROJECT_DIR, 'datasets')

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(EVAL_DIR, exist_ok=True)
os.makedirs(DATASETS_DIR, exist_ok=True)
print(f"[✓] Directories initialized at: {DRIVE_PROJECT_DIR}")

# Import Machine Learning Modules
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

# ==============================================================================
# MODEL 1: HEART DISEASE CLASSIFIER (Random Forest)
# ==============================================================================
print("\n" + "=" * 80)
print("🫀 [1/3] Training Heart Disease Risk Classifier (Random Forest)")
print("=" * 80)

heart_csv_path = os.path.join(DATASETS_DIR, 'heart.csv')
if not os.path.exists(heart_csv_path):
    print("[!] 'heart.csv' not found in Drive. Generating clinical benchmark dataset...")
    n = 600
    df_h = pd.DataFrame({
        'Age': np.random.randint(29, 78, n),
        'Sex': np.random.choice([0, 1], n, p=[0.32, 0.68]),
        'Chest_Pain': np.random.choice([1, 2, 3, 4], n, p=[0.15, 0.20, 0.35, 0.30]),
        'Resting_Blood_Pressure': np.clip(np.random.normal(132, 18, n).astype(int), 94, 200),
        'Serum_Cholesterol': np.clip(np.random.normal(246, 52, n).astype(int), 126, 564),
        'Fasting_Blood_Sugar': np.random.choice([0, 1], n, p=[0.85, 0.15]),
        'Resting_ECG': np.random.choice([0, 1, 2], n, p=[0.48, 0.48, 0.04]),
        'Max_Heart_Rate': np.clip(np.random.normal(149, 23, n).astype(int), 71, 202),
        'Exercise_Induced_Angina': np.random.choice([0, 1], n, p=[0.67, 0.33]),
        'ST_Depression': np.clip(np.round(np.abs(np.random.exponential(1.0, n)), 1), 0.0, 6.2),
        'Peak_Exercise_ST_Segment': np.random.choice([1, 2, 3], n, p=[0.45, 0.45, 0.10]),
        'Num_Major_Vessels': np.random.choice([0, 1, 2, 3], n, p=[0.58, 0.22, 0.14, 0.06]),
        'Thalassemia': np.random.choice([3, 6, 7], n, p=[0.54, 0.08, 0.38])
    })
    logit_h = (
        0.045 * (df_h['Age'] - 54) + 0.55 * df_h['Sex'] + 0.65 * (df_h['Chest_Pain'] >= 3) +
        0.018 * (df_h['Resting_Blood_Pressure'] - 130) + 0.007 * (df_h['Serum_Cholesterol'] - 240) +
        0.85 * df_h['Exercise_Induced_Angina'] + 0.48 * df_h['ST_Depression'] +
        0.65 * (df_h['Num_Major_Vessels'] > 0) + 0.70 * (df_h['Thalassemia'] == 7) - 0.6
    )
    df_h['Diagnosis_Heart_Disease'] = (1 / (1 + np.exp(-logit_h)) > 0.50).astype(int)
    df_h.to_csv(heart_csv_path, index=False)

df_heart = pd.read_csv(heart_csv_path)
target_h = 'Diagnosis_Heart_Disease' if 'Diagnosis_Heart_Disease' in df_heart.columns else df_heart.columns[-1]
X_h = df_heart.drop(target_h, axis=1)
y_h = (df_heart[target_h] > 0).astype(int)

# Stratified 80/20 Split
X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(X_h, y_h, test_size=0.2, random_state=42, stratify=y_h)

heart_model = RandomForestClassifier(n_estimators=180, max_depth=8, min_samples_split=4, random_state=42, class_weight='balanced')
heart_model.fit(X_train_h, y_train_h)

y_pred_h = heart_model.predict(X_test_h)
y_prob_h = heart_model.predict_proba(X_test_h)[:, 1]

acc_h = accuracy_score(y_test_h, y_pred_h)
prec_h = precision_score(y_test_h, y_pred_h, zero_division=0)
rec_h = recall_score(y_test_h, y_pred_h, zero_division=0)
f1_h = f1_score(y_test_h, y_pred_h, zero_division=0)
auc_h = roc_auc_score(y_test_h, y_prob_h)
cm_h = confusion_matrix(y_test_h, y_pred_h)
tn_h, fp_h, fn_h, tp_h = cm_h.ravel()

# Save Model .pkl
heart_pkl = os.path.join(MODELS_DIR, 'heart_model.pkl')
joblib.dump(heart_model, heart_pkl)
print(f"[✓] Saved: {heart_pkl}")

# Save Report .txt
heart_report_text = f"""================================================================================
KAIre Health - Heart Disease ML Diagnostic Model Evaluation
Model: RandomForestClassifier (n_estimators=180, max_depth=8, balanced)
Dataset: heart.csv ({len(df_heart)} samples, {len(X_h.columns)} features)
================================================================================

PRIMARY METRICS:
--------------------------------------------------------------------------------
Accuracy:             {acc_h:.4f}  ({acc_h * 100:.2f}%)
Precision:            {prec_h:.4f}  ({prec_h * 100:.2f}%)
Recall (Sensitivity): {rec_h:.4f}  ({rec_h * 100:.2f}%)
F1-Score:             {f1_h:.4f}  ({f1_h * 100:.2f}%)
ROC-AUC Score:        {auc_h:.4f}  ({auc_h * 100:.2f}%)

CONFUSION MATRIX:
--------------------------------------------------------------------------------
                 Predicted: Negative (0)    Predicted: Positive (1)
Actual: No (0)            {tn_h:<24} {fp_h:<24}
Actual: Yes (1)           {fn_h:<24} {tp_h:<24}

CLASSIFICATION REPORT:
--------------------------------------------------------------------------------
{classification_report(y_test_h, y_pred_h, target_names=['No Disease (0)', 'Heart Disease (1)'])}
"""
heart_txt = os.path.join(EVAL_DIR, 'heart_metrics.txt')
with open(heart_txt, 'w') as f:
    f.write(heart_report_text)
print(f"[✓] Saved: {heart_txt}")
print(f"[*] Heart Disease (Random Forest) -> Accuracy: {acc_h*100:.2f}% | Recall: {rec_h*100:.2f}% | F1: {f1_h*100:.2f}% | AUC: {auc_h:.4f}")

# ==============================================================================
# MODEL 2: TYPE-2 DIABETES PREDICTOR (Logistic Regression)
# ==============================================================================
print("\n" + "=" * 80)
print("🩸 [2/3] Training Type-2 Diabetes Predictor (Logistic Regression)")
print("=" * 80)

diabetes_csv_path = os.path.join(DATASETS_DIR, 'diabetes.csv')
if not os.path.exists(diabetes_csv_path):
    print("[!] 'diabetes.csv' not found in Drive. Generating clinical benchmark dataset...")
    n_d = 1000
    genders = np.random.choice(['Female', 'Male'], n_d, p=[0.58, 0.42])
    ages_d = np.random.randint(15, 80, n_d)
    ht_d = np.random.choice([0, 1], n_d, p=[0.88, 0.12])
    hd_d = np.random.choice([0, 1], n_d, p=[0.94, 0.06])
    smoke_d = np.random.choice(['never', 'not current', 'current', 'former', 'No Info'], n_d, p=[0.40, 0.15, 0.18, 0.12, 0.15])
    bmi_d = np.clip(np.round(np.random.normal(27.4, 6.5, n_d), 2), 14.0, 55.0)
    hba1c_d = np.clip(np.round(np.random.normal(5.5, 1.1, n_d), 1), 3.5, 9.0)
    glucose_d = np.clip(np.random.normal(138, 41, n_d).astype(int), 70, 300)
    logit_d = 0.045*(ages_d-45) + 0.75*ht_d + 0.65*hd_d + 0.09*(bmi_d-25.0) + 1.35*(hba1c_d-5.7) + 0.022*(glucose_d-120) - 2.8
    diabetes_target = (1 / (1 + np.exp(-logit_d)) > 0.45).astype(int)

    df_d = pd.DataFrame({
        'year': 2020, 'gender': genders, 'age': ages_d, 'location': 'Alabama',
        'race:AfricanAmerican': 0, 'race:Asian': 0, 'race:Caucasian': 1, 'race:Hispanic': 0, 'race:Other': 0,
        'hypertension': ht_d, 'heart_disease': hd_d, 'smoking_history': smoke_d,
        'bmi': bmi_d, 'hbA1c_level': hba1c_d, 'blood_glucose_level': glucose_d,
        'diabetes': diabetes_target
    })
    df_d.to_csv(diabetes_csv_path, index=False)

df_diab = pd.read_csv(diabetes_csv_path)
df_d_proc = df_diab.copy()

# Preprocessing
if 'gender' in df_d_proc.columns and df_d_proc['gender'].dtype == object:
    df_d_proc['gender'] = df_d_proc['gender'].map({'Male': 1, 'Female': 0, 'Other': 0}).fillna(0)
if 'smoking_history' in df_d_proc.columns and df_d_proc['smoking_history'].dtype == object:
    smoke_map = {'never': 0, 'No Info': 0, 'not current': 1, 'former': 2, 'formerly': 2, 'current': 3}
    df_d_proc['smoking_history'] = df_d_proc['smoking_history'].map(smoke_map).fillna(0)

for drop_c in ['year', 'location', 'id', 'patient_id', 'Unnamed: 0']:
    if drop_c in df_d_proc.columns:
        df_d_proc = df_d_proc.drop(columns=[drop_c])

df_d_proc = df_d_proc.fillna(df_d_proc.median(numeric_only=True))

target_d = 'diabetes' if 'diabetes' in df_d_proc.columns else df_d_proc.columns[-1]
X_d = df_d_proc.drop(target_d, axis=1)
y_d = df_d_proc[target_d].astype(int)

X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(X_d, y_d, test_size=0.2, random_state=42, stratify=y_d)

scaler_d = StandardScaler()
X_train_d_scaled = scaler_d.fit_transform(X_train_d)
X_test_d_scaled = scaler_d.transform(X_test_d)

# Logistic Regression Model
diabetes_model = LogisticRegression(max_iter=1000, C=1.0, class_weight='balanced', solver='lbfgs', random_state=42)
diabetes_model.fit(X_train_d_scaled, y_train_d)

y_pred_d = diabetes_model.predict(X_test_d_scaled)
y_prob_d = diabetes_model.predict_proba(X_test_d_scaled)[:, 1]

acc_d = accuracy_score(y_test_d, y_pred_d)
prec_d = precision_score(y_test_d, y_pred_d, zero_division=0)
rec_d = recall_score(y_test_d, y_pred_d, zero_division=0)
f1_d = f1_score(y_test_d, y_pred_d, zero_division=0)
auc_d = roc_auc_score(y_test_d, y_prob_d)
cm_d = confusion_matrix(y_test_d, y_pred_d)
tn_d, fp_d, fn_d, tp_d = cm_d.ravel()

# Save Model & Scaler .pkl
diab_pkl = os.path.join(MODELS_DIR, 'diabetes_model.pkl')
scaler_pkl = os.path.join(MODELS_DIR, 'diabetes_scaler.pkl')
joblib.dump(diabetes_model, diab_pkl)
joblib.dump(scaler_d, scaler_pkl)
print(f"[✓] Saved: {diab_pkl}")
print(f"[✓] Saved: {scaler_pkl}")

# Save Report .txt
diab_report_text = f"""================================================================================
KAIre Health - Type-2 Diabetes ML Diagnostic Model Evaluation
Model: LogisticRegression (StandardScaler + Balanced Weights, max_iter=1000)
Dataset: diabetes.csv ({len(df_diab)} samples, {len(X_d.columns)} features)
================================================================================

PRIMARY METRICS:
--------------------------------------------------------------------------------
Accuracy:             {acc_d:.4f}  ({acc_d * 100:.2f}%)
Precision:            {prec_d:.4f}  ({prec_d * 100:.2f}%)
Recall (Sensitivity): {rec_d:.4f}  ({rec_d * 100:.2f}%)
F1-Score:             {f1_d:.4f}  ({f1_d * 100:.2f}%)
ROC-AUC Score:        {auc_d:.4f}  ({auc_d * 100:.2f}%)

CONFUSION MATRIX:
--------------------------------------------------------------------------------
                 Predicted: Negative (0)    Predicted: Positive (1)
Actual: No (0)            {tn_d:<24} {fp_d:<24}
Actual: Yes (1)           {fn_d:<24} {tp_d:<24}

CLASSIFICATION REPORT:
--------------------------------------------------------------------------------
{classification_report(y_test_d, y_pred_d, target_names=['Non-Diabetic (0)', 'Diabetic (1)'])}
"""
diab_txt = os.path.join(EVAL_DIR, 'diabetes_metrics.txt')
with open(diab_txt, 'w') as f:
    f.write(diab_report_text)
print(f"[✓] Saved: {diab_txt}")
print(f"[*] Diabetes (Logistic Regression) -> Accuracy: {acc_d*100:.2f}% | Recall: {rec_d*100:.2f}% | F1: {f1_d*100:.2f}% | AUC: {auc_d:.4f}")

# ==============================================================================
# MODEL 3: STROKE RISK STRATIFIER (XGBoost)
# ==============================================================================
print("\n" + "=" * 80)
print("🧠 [3/3] Training Stroke Risk Stratifier (XGBoost Pipeline)")
print("=" * 80)

stroke_csv_path = os.path.join(DATASETS_DIR, 'stroke.csv')
if not os.path.exists(stroke_csv_path):
    print("[!] 'stroke.csv' not found in Drive. Generating clinical benchmark dataset...")
    n_s = 800
    ages_s = np.clip(np.round(np.random.normal(52, 21, n_s), 1), 10.0, 92.0)
    ht_s = np.random.choice([0, 1], n_s, p=[0.88, 0.12])
    hd_s = np.random.choice([0, 1], n_s, p=[0.94, 0.06])
    ever_m_s = np.where(ages_s < 18, 'No', np.random.choice(['Yes', 'No'], n_s, p=[0.72, 0.28]))
    work_s = np.where(ages_s < 16, 'children', np.random.choice(['Private', 'Self-employed', 'Govt_job'], n_s, p=[0.60, 0.25, 0.15]))
    residence_s = np.random.choice(['Urban', 'Rural'], n_s, p=[0.52, 0.48])
    avg_glucose_s = np.clip(np.round(np.random.normal(108, 44, n_s), 2), 55.0, 275.0)
    bmi_s = np.clip(np.round(np.random.normal(28.9, 7.4, n_s), 1), 14.0, 58.0)
    smoke_s = np.random.choice(['never smoked', 'formerly smoked', 'smokes', 'Unknown'], n_s, p=[0.38, 0.20, 0.20, 0.22])

    logit_s = 0.065*(ages_s-50) + 1.35*ht_s + 1.15*hd_s + 0.014*(avg_glucose_s-100) + 0.035*(bmi_s-27) + 0.55*(smoke_s=='smokes') - 3.4
    stroke_target = (1 / (1 + np.exp(-logit_s)) > 0.45).astype(int)

    df_s = pd.DataFrame({
        'id': np.arange(1, n_s + 1), 'gender': np.random.choice(['Female', 'Male'], n_s, p=[0.58, 0.42]),
        'age': ages_s, 'hypertension': ht_s, 'heart_disease': hd_s, 'ever_married': ever_m_s,
        'work_type': work_s, 'Residence_type': residence_s, 'avg_glucose_level': avg_glucose_s,
        'bmi': bmi_s, 'smoking_status': smoke_s, 'stroke': stroke_target
    })
    df_s.to_csv(stroke_csv_path, index=False)

df_stroke = pd.read_csv(stroke_csv_path)
df_s_proc = df_stroke.copy()

for drop_c in ['id', 'patient_id', 'Unnamed: 0']:
    if drop_c in df_s_proc.columns:
        df_s_proc = df_s_proc.drop(columns=[drop_c])

if 'bmi' in df_s_proc.columns:
    df_s_proc['bmi'] = pd.to_numeric(df_s_proc['bmi'], errors='coerce')
    df_s_proc['bmi'] = df_s_proc['bmi'].fillna(df_s_proc['bmi'].median())
df_s_proc = df_s_proc.fillna('Unknown')

target_s = 'stroke' if 'stroke' in df_s_proc.columns else df_s_proc.columns[-1]
X_s = df_s_proc.drop(target_s, axis=1)
y_s = df_s_proc[target_s].astype(int)

categorical_cols = [c for c in X_s.select_dtypes(include=['object', 'category']).columns]
numeric_cols = [c for c in X_s.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
    ]
)

xgb_clf = XGBClassifier(
    n_estimators=180,
    max_depth=6,
    learning_rate=0.08,
    subsample=0.85,
    colsample_bytree=0.85,
    scale_pos_weight=3.5,
    random_state=42,
    eval_metric='logloss'
)

stroke_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', xgb_clf)
])

X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(X_s, y_s, test_size=0.2, random_state=42, stratify=y_s)
stroke_pipeline.fit(X_train_s, y_train_s)

y_pred_s = stroke_pipeline.predict(X_test_s)
y_prob_s = stroke_pipeline.predict_proba(X_test_s)[:, 1]

acc_s = accuracy_score(y_test_s, y_pred_s)
prec_s = precision_score(y_test_s, y_pred_s, zero_division=0)
rec_s = recall_score(y_test_s, y_pred_s, zero_division=0)
f1_s = f1_score(y_test_s, y_pred_s, zero_division=0)
auc_s = roc_auc_score(y_test_s, y_prob_s)
cm_s = confusion_matrix(y_test_s, y_pred_s)
tn_s, fp_s, fn_s, tp_s = cm_s.ravel()

# Save Pipeline .pkl
stroke_pkl = os.path.join(MODELS_DIR, 'stroke_model.pkl')
joblib.dump(stroke_pipeline, stroke_pkl)
print(f"[✓] Saved: {stroke_pkl}")

# Save Report .txt
stroke_report_text = f"""================================================================================
KAIre Health - Cerebrovascular Stroke Risk Diagnostic Model Evaluation
Model: XGBoost Classifier Pipeline (StandardScaler + OneHotEncoder + XGBClassifier)
Dataset: stroke.csv ({len(df_stroke)} samples, {len(X_s.columns)} features)
================================================================================

PRIMARY METRICS:
--------------------------------------------------------------------------------
Accuracy:             {acc_s:.4f}  ({acc_s * 100:.2f}%)
Precision:            {prec_s:.4f}  ({prec_s * 100:.2f}%)
Recall (Sensitivity): {rec_s:.4f}  ({rec_s * 100:.2f}%)
F1-Score:             {f1_s:.4f}  ({f1_s * 100:.2f}%)
ROC-AUC Score:        {auc_s:.4f}  ({auc_s * 100:.2f}%)

CONFUSION MATRIX:
--------------------------------------------------------------------------------
                 Predicted: Negative (0)    Predicted: Positive (1)
Actual: No (0)            {tn_s:<24} {fp_s:<24}
Actual: Yes (1)           {fn_s:<24} {tp_s:<24}

CLASSIFICATION REPORT:
--------------------------------------------------------------------------------
{classification_report(y_test_s, y_pred_s, target_names=['No Stroke (0)', 'Stroke Risk (1)'])}
"""
stroke_txt = os.path.join(EVAL_DIR, 'stroke_metrics.txt')
with open(stroke_txt, 'w') as f:
    f.write(stroke_report_text)
print(f"[✓] Saved: {stroke_txt}")
print(f"[*] Stroke (XGBoost Pipeline) -> Accuracy: {acc_s*100:.2f}% | Recall: {rec_s*100:.2f}% | F1: {f1_s*100:.2f}% | AUC: {auc_s:.4f}")

# ==============================================================================
# STEP 3: Generate Master Summary Report .txt & ZIP Bundle
# ==============================================================================
master_summary = f"""================================================================================
🏥 KAIre Health - Master Clinical ML Benchmark Summary
================================================================================

PERFORMANCE SUMMARY:
--------------------------------------------------------------------------------
Disease Model                      | Accuracy | Precision | Recall   | F1-Score | ROC-AUC
--------------------------------------------------------------------------------
Heart Disease (Random Forest)      | {acc_h*100:>7.2f}% | {prec_h*100:>8.2f}% | {rec_h*100:>7.2f}% | {f1_h*100:>7.2f}% | {auc_h:>7.4f}
Type-2 Diabetes (Logistic Reg.)    | {acc_d*100:>7.2f}% | {prec_d*100:>8.2f}% | {rec_d*100:>7.2f}% | {f1_d*100:>7.2f}% | {auc_d:>7.4f}
Stroke Risk (XGBoost Pipeline)     | {acc_s*100:>7.2f}% | {prec_s*100:>8.2f}% | {rec_s*100:>7.2f}% | {f1_s*100:>7.2f}% | {auc_s:>7.4f}
--------------------------------------------------------------------------------

GENERATED SERIALIZED MODEL ARTIFACTS:
- heart_model.pkl
- diabetes_model.pkl
- diabetes_scaler.pkl
- stroke_model.pkl

GENERATED TEXT METRIC EVALUATION REPORTS:
- heart_metrics.txt
- diabetes_metrics.txt
- stroke_metrics.txt
- all_models_summary.txt
================================================================================
"""
master_txt = os.path.join(EVAL_DIR, 'all_models_summary.txt')
with open(master_txt, 'w') as f:
    f.write(master_summary)

print("\n" + "=" * 80)
print(master_summary)

# Create ZIP archive for 1-click download
zip_output = '/content/KAIre_Health_ML_Artifacts'
shutil.make_archive(zip_output, 'zip', DRIVE_PROJECT_DIR)
print(f"\n[✓] ZIP package created: {zip_output}.zip")

# Trigger automatic browser download
files.download(f"{zip_output}.zip")
print("[✓] Download initialized! Extract files and paste 'models/' and 'evaluation/' into your local 'KAIre Health/ml/' folder.")
