import math

def calculate_preeclampsia_risk(entities):
    age = entities.get('age', 30)
    bmi = entities.get('bmi', 25)
    blood_pressure = entities.get('blood_pressure', '120/80')
    family_history = 1 if 'preeclampsia' in entities.get('family_history', []) else 0
    
    systolic, diastolic = map(int, blood_pressure.split('/'))
    
    risk = (
        -6.7 + 
        0.1 * age + 
        0.1 * bmi + 
        0.05 * systolic + 
        0.1 * family_history
    )
    
    risk_percentage = 1 / (1 + math.exp(-risk)) * 100
    return {"risk": f"{risk_percentage:.2f}%"}

def calculate_gestational_diabetes_risk(entities):
    age = entities.get('age', 30)
    bmi = entities.get('bmi', 25)
    family_history = 1 if 'diabetes' in entities.get('family_history', []) else 0
    
    risk = (
        -5.1 + 
        0.1 * age + 
        0.2 * bmi + 
        1.5 * family_history
    )
    
    risk_percentage = 1 / (1 + math.exp(-risk)) * 100
    return {"risk": f"{risk_percentage:.2f}%"}

# Implement other risk calculation functions similarly

def calculate_risks(entities, risk_type):
    risk_functions = {
        "preeclampsia": calculate_preeclampsia_risk,
        "gestational_diabetes": calculate_gestational_diabetes_risk,
        # Add other risk functions here
    }
    
    if risk_type in risk_functions:
        return risk_functions[risk_type](entities)
    else:
        return {"risk": "Unknown risk type"}