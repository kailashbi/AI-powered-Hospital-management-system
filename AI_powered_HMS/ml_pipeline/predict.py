"""
predict.py — loads saved .pkl models and runs inference.

Heart model uses get_dummies encoding so we need heart_features.pkl
to ensure correct column alignment at prediction time.
"""
import os, joblib, numpy as np, pandas as pd

_BASE  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODEL = os.path.join(_BASE, "model")

_heart_model    = None
_heart_features = None   # list of feature column names after get_dummies
_diabetes_model = None
_diabetes_scaler= None
_stroke_model   = None


def _load_heart():
    global _heart_model, _heart_features
    if _heart_model is None:
        _heart_model    = joblib.load(os.path.join(_MODEL, "heart_model.pkl"))
        _heart_features = joblib.load(os.path.join(_MODEL, "heart_features.pkl"))
    return _heart_model, _heart_features


def _load_diabetes():
    global _diabetes_model, _diabetes_scaler
    if _diabetes_model is None:
        _diabetes_model  = joblib.load(os.path.join(_MODEL, "diabetes_model.pkl"))
        _diabetes_scaler = joblib.load(os.path.join(_MODEL, "diabetes_scaler.pkl"))
    return _diabetes_model, _diabetes_scaler


def _load_stroke():
    global _stroke_model
    if _stroke_model is None:
        _stroke_model = joblib.load(os.path.join(_MODEL, "stroke_model.pkl"))
    return _stroke_model


def predict_heart(age, sex, cp, trestbps, chol, fbs, restecg,
                  thalch, exang, oldpeak, slope, ca, thal):
    """
    Pass individual field values (all numeric / already encoded).
    Returns (prediction: int, probability: float)
    """
    model, features = _load_heart()

    # Build a DataFrame with the same columns the model was trained on.
    # The training used pd.get_dummies on sex, cp, fbs, restecg, exang, slope, thal.
    # We pass numeric codes so get_dummies just keeps them as-is (already int).
    row = pd.DataFrame([{
        "age": age, "sex": sex, "cp": cp, "trestbps": trestbps,
        "chol": chol, "fbs": fbs, "restecg": restecg, "thalch": thalch,
        "exang": exang, "oldpeak": oldpeak, "slope": slope, "ca": ca, "thal": thal
    }])

    # Align to training feature list — fill missing dummy cols with 0
    row = row.reindex(columns=features, fill_value=0)

    pred = int(model.predict(row)[0])
    prob = float(model.predict_proba(row)[0][1])
    return pred, prob


def predict_diabetes(pregnancies, glucose, blood_pressure, skin_thickness,
                     insulin, bmi, diabetes_pedigree, age):
    """Returns (prediction: int, probability: float)"""
    model, scaler = _load_diabetes()
    data   = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                        insulin, bmi, diabetes_pedigree, age]])
    scaled = scaler.transform(data)
    pred   = int(model.predict(scaled)[0])
    prob   = float(model.predict_proba(scaled)[0][1])
    return pred, prob


def predict_stroke(gender, age, hypertension, heart_disease, ever_married,
                   work_type, residence_type, avg_glucose, bmi, smoking_status):
    """Returns (prediction: int, probability: float)"""
    model = _load_stroke()
    data  = np.array([[gender, age, hypertension, heart_disease, ever_married,
                       work_type, residence_type, avg_glucose, bmi, smoking_status]])
    pred  = int(model.predict(data)[0])
    prob  = float(model.predict_proba(data)[0][1])
    return pred, prob