import numpy as np
import pandas as pd
import os

def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    datasets_dir = os.path.join(base_dir, 'datasets')
    models_dir = os.path.join(base_dir, 'models')
    eval_dir = os.path.join(base_dir, 'evaluation')

    os.makedirs(datasets_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(eval_dir, exist_ok=True)

    np.random.seed(42)

    # =========================================================================
    # 1. Heart Disease Dataset (Exact Match with Image 1)
    # Columns: Age, Sex, Chest_Pain, Resting_Blood_Pressure, Serum_Cholesterol,
    # Fasting_Blood_Sugar, Resting_ECG, Max_Heart_Rate, Exercise_Induced_Angina,
    # ST_Depression, Peak_Exercise_ST_Segment, Num_Major_Vessels, Thalassemia,
    # Diagnosis_Heart_Disease
    # =========================================================================
    n_heart = 600
    age_h = np.random.randint(29, 78, n_heart)
    sex_h = np.random.choice([0, 1], n_heart, p=[0.32, 0.68])
    # Chest_Pain: 1: Typical Angina, 2: Atypical Angina, 3: Non-Anginal, 4: Asymptomatic
    cp_h = np.random.choice([1, 2, 3, 4], n_heart, p=[0.15, 0.20, 0.35, 0.30])
    trestbps_h = np.random.normal(132, 18, n_heart).astype(int)
    trestbps_h = np.clip(trestbps_h, 94, 200)
    chol_h = np.random.normal(246, 52, n_heart).astype(int)
    chol_h = np.clip(chol_h, 126, 564)
    fbs_h = np.random.choice([0, 1], n_heart, p=[0.85, 0.15])
    restecg_h = np.random.choice([0, 1, 2], n_heart, p=[0.48, 0.48, 0.04])
    thalach_h = np.random.normal(149, 23, n_heart).astype(int)
    thalach_h = np.clip(thalach_h, 71, 202)
    exang_h = np.random.choice([0, 1], n_heart, p=[0.67, 0.33])
    oldpeak_h = np.round(np.abs(np.random.exponential(1.0, n_heart)), 1)
    oldpeak_h = np.clip(oldpeak_h, 0.0, 6.2)
    # Peak_Exercise_ST_Segment (Slope): 1: Upsloping, 2: Flat, 3: Downsloping
    slope_h = np.random.choice([1, 2, 3], n_heart, p=[0.45, 0.45, 0.10])
    # Num_Major_Vessels: 0, 1, 2, 3
    ca_h = np.random.choice([0, 1, 2, 3], n_heart, p=[0.58, 0.22, 0.14, 0.06])
    # Thalassemia: 3: Normal, 6: Fixed Defect, 7: Reversible Defect
    thal_h = np.random.choice([3, 6, 7], n_heart, p=[0.54, 0.08, 0.38])

    logit_h = (
        0.045 * (age_h - 54) +
        0.55 * sex_h +
        0.65 * (cp_h >= 3) +
        0.018 * (trestbps_h - 130) +
        0.007 * (chol_h - 240) +
        0.35 * fbs_h +
        -0.028 * (thalach_h - 150) +
        0.85 * exang_h +
        0.48 * oldpeak_h +
        0.65 * (ca_h > 0) +
        0.70 * (thal_h == 7) - 0.6
    )
    prob_h = 1 / (1 + np.exp(-logit_h))
    target_h = (prob_h > 0.50).astype(int)

    df_heart = pd.DataFrame({
        'Age': age_h,
        'Sex': sex_h,
        'Chest_Pain': cp_h,
        'Resting_Blood_Pressure': trestbps_h,
        'Serum_Cholesterol': chol_h,
        'Fasting_Blood_Sugar': fbs_h,
        'Resting_ECG': restecg_h,
        'Max_Heart_Rate': thalach_h,
        'Exercise_Induced_Angina': exang_h,
        'ST_Depression': oldpeak_h,
        'Peak_Exercise_ST_Segment': slope_h,
        'Num_Major_Vessels': ca_h,
        'Thalassemia': thal_h,
        'Diagnosis_Heart_Disease': target_h
    })
    heart_file = os.path.join(datasets_dir, 'heart.csv')
    df_heart.to_csv(heart_file, index=False)
    print(f"[✓] Generated Heart Dataset matching Image 1: {heart_file} ({len(df_heart)} rows)")

    # =========================================================================
    # 2. Diabetes Prediction Dataset (Exact Match with Image 2)
    # Columns: year, gender, age, location, race:AfricanAmerican, race:Asian,
    # race:Caucasian, race:Hispanic, race:Other, hypertension, heart_disease,
    # smoking_history, bmi, hbA1c_level, blood_glucose_level, diabetes
    # =========================================================================
    n_diab = 1000
    years = np.random.choice([2015, 2016, 2017, 2018, 2019, 2020], n_diab)
    genders = np.random.choice(['Female', 'Male'], n_diab, p=[0.58, 0.42])
    ages_d = np.random.randint(15, 80, n_diab)
    locations = np.random.choice(['Alabama', 'California', 'Texas', 'Florida', 'New York', 'Ohio'], n_diab)
    
    # Demographics
    races = np.random.choice(['Caucasian', 'AfricanAmerican', 'Asian', 'Hispanic', 'Other'], n_diab, p=[0.65, 0.15, 0.08, 0.08, 0.04])
    race_af = (races == 'AfricanAmerican').astype(int)
    race_as = (races == 'Asian').astype(int)
    race_ca = (races == 'Caucasian').astype(int)
    race_hi = (races == 'Hispanic').astype(int)
    race_ot = (races == 'Other').astype(int)

    ht_d = np.random.choice([0, 1], n_diab, p=[0.88, 0.12])
    hd_d = np.random.choice([0, 1], n_diab, p=[0.94, 0.06])
    smoking_h = np.random.choice(['never', 'not current', 'current', 'former', 'No Info'], n_diab, p=[0.40, 0.15, 0.18, 0.12, 0.15])
    
    bmi_d = np.round(np.random.normal(27.4, 6.5, n_diab), 2)
    bmi_d = np.clip(bmi_d, 14.0, 55.0)

    # HbA1c Level: Normal 4.0 - 5.6%, Prediabetes 5.7 - 6.4%, Diabetes >= 6.5%
    hba1c_d = np.round(np.random.normal(5.5, 1.1, n_diab), 1)
    hba1c_d = np.clip(hba1c_d, 3.5, 9.0)

    # Blood Glucose Level: Normal 70-99 mg/dL, Prediabetes 100-125, Diabetes >= 126
    glucose_d = np.random.normal(138, 41, n_diab).astype(int)
    glucose_d = np.clip(glucose_d, 70, 300)

    logit_d = (
        0.045 * (ages_d - 45) +
        0.75 * ht_d +
        0.65 * hd_d +
        0.09 * (bmi_d - 25.0) +
        1.35 * (hba1c_d - 5.7) +
        0.022 * (glucose_d - 120) +
        0.30 * (smoking_h == 'current') - 2.8
    )
    prob_d = 1 / (1 + np.exp(-logit_d))
    diabetes_target = (prob_d > 0.45).astype(int)

    df_diab = pd.DataFrame({
        'year': years,
        'gender': genders,
        'age': ages_d,
        'location': locations,
        'race:AfricanAmerican': race_af,
        'race:Asian': race_as,
        'race:Caucasian': race_ca,
        'race:Hispanic': race_hi,
        'race:Other': race_ot,
        'hypertension': ht_d,
        'heart_disease': hd_d,
        'smoking_history': smoking_h,
        'bmi': bmi_d,
        'hbA1c_level': hba1c_d,
        'blood_glucose_level': glucose_d,
        'diabetes': diabetes_target
    })
    diabetes_file = os.path.join(datasets_dir, 'diabetes.csv')
    df_diab.to_csv(diabetes_file, index=False)
    print(f"[✓] Generated Diabetes Dataset matching Image 2: {diabetes_file} ({len(df_diab)} rows)")

    # =========================================================================
    # 3. Stroke Prediction Dataset (Exact Match with Image 3)
    # Columns: id, gender, age, hypertension, heart_disease, ever_married,
    # work_type, Residence_type, avg_glucose_level, bmi, smoking_status, stroke
    # =========================================================================
    n_stroke = 800
    ids_s = np.arange(1, n_stroke + 1)
    genders_s = np.random.choice(['Female', 'Male'], n_stroke, p=[0.58, 0.42])
    ages_s = np.round(np.random.normal(52, 21, n_stroke), 1)
    ages_s = np.clip(ages_s, 10.0, 92.0)
    ht_s = np.random.choice([0, 1], n_stroke, p=[0.88, 0.12])
    hd_s = np.random.choice([0, 1], n_stroke, p=[0.94, 0.06])
    ever_m_s = np.where(ages_s < 18, 'No', np.random.choice(['Yes', 'No'], n_stroke, p=[0.72, 0.28]))
    work_s = np.where(ages_s < 16, 'children', np.random.choice(['Private', 'Self-employed', 'Govt_job'], n_stroke, p=[0.60, 0.25, 0.15]))
    residence_s = np.random.choice(['Urban', 'Rural'], n_stroke, p=[0.52, 0.48])
    
    avg_glucose_s = np.round(np.random.normal(108, 44, n_stroke), 2)
    avg_glucose_s = np.clip(avg_glucose_s, 55.0, 275.0)
    
    bmi_s = np.round(np.random.normal(28.9, 7.4, n_stroke), 1)
    bmi_s = np.clip(bmi_s, 14.0, 58.0)
    
    smoking_s = np.random.choice(['never smoked', 'formerly smoked', 'smokes', 'Unknown'], n_stroke, p=[0.38, 0.20, 0.20, 0.22])

    logit_s = (
        0.065 * (ages_s - 50) +
        1.35 * ht_s +
        1.15 * hd_s +
        0.014 * (avg_glucose_s - 100) +
        0.035 * (bmi_s - 27) +
        0.55 * (smoking_s == 'smokes') +
        0.35 * (smoking_s == 'formerly smoked') - 3.4
    )
    prob_s = 1 / (1 + np.exp(-logit_s))
    stroke_target = (prob_s > 0.45).astype(int)

    df_stroke = pd.DataFrame({
        'id': ids_s,
        'gender': genders_s,
        'age': ages_s,
        'hypertension': ht_s,
        'heart_disease': hd_s,
        'ever_married': ever_m_s,
        'work_type': work_s,
        'Residence_type': residence_s,
        'avg_glucose_level': avg_glucose_s,
        'bmi': bmi_s,
        'smoking_status': smoking_s,
        'stroke': stroke_target
    })
    stroke_file = os.path.join(datasets_dir, 'stroke.csv')
    df_stroke.to_csv(stroke_file, index=False)
    print(f"[✓] Generated Stroke Dataset matching Image 3: {stroke_file} ({len(df_stroke)} rows)")

if __name__ == '__main__':
    main()
