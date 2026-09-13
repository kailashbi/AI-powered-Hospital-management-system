import re

def validate_email(email: str) -> bool:
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email.strip()))

def validate_vital_ranges(temp, bp_sys, bp_dia, hr, spo2, weight):
    errors = []
    if temp < 85.0 or temp > 115.0:
        errors.append("Body temperature must be between 85.0°F and 115.0°F.")
    if bp_sys < 50 or bp_sys > 260:
        errors.append("Systolic blood pressure must be between 50 and 260 mmHg.")
    if bp_dia < 30 or bp_dia > 160:
        errors.append("Diastolic blood pressure must be between 30 and 160 mmHg.")
    if hr < 30 or hr > 240:
        errors.append("Heart rate must be between 30 and 240 BPM.")
    if spo2 < 50 or spo2 > 100:
        errors.append("Oxygen saturation (SpO2) must be between 50% and 100%.")
    if weight <= 0 or weight > 500:
        errors.append("Patient weight must be a positive number under 500 kg.")
    return errors
