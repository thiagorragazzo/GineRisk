class GynRiskCalculator:
    def calculate_preeclampsia_risk(self, data):
        risk_score = 0
        if data["idade"] > 35:
            risk_score += 1
        if data["imc"] > 30:
            risk_score += 1
        if "hipertensao" in data["condicoes_preexistentes"]:
            risk_score += 2
        if "preeclampsia_anterior" in data["historico_familiar"]:
            risk_score += 2
        
        risk_level = "Baixo"
        if risk_score > 3:
            risk_level = "Alto"
        elif risk_score > 1:
            risk_level = "Moderado"
        
        return {"risk_score": risk_score, "risk_level": risk_level}

    def calculate_gestational_diabetes_risk(self, data):
        risk_score = 0
        if data["idade"] > 25:
            risk_score += 1
        if data["imc"] > 25:
            risk_score += 1
        if "diabetes_gestacional_anterior" in data["historico_familiar"]:
            risk_score += 2
        if "diabetes_tipo2" in data["historico_familiar"]:
            risk_score += 1
        
        risk_level = "Baixo"
        if risk_score > 3:
            risk_level = "Alto"
        elif risk_score > 1:
            risk_level = "Moderado"
        
        return {"risk_score": risk_score, "risk_level": risk_level}
