class GynRiskCalculator:
    def calculate_preeclampsia_risk(self, data):
        risk_score = 0
        
        # Verifica se a idade está presente e é um número válido
        if data.get("idade") is not None:
            try:
                idade = int(data["idade"])
                if idade > 35:
                    risk_score += 1
            except ValueError:
                print(f"Aviso: Idade inválida: {data['idade']}")
        
        # Verifica se o IMC está presente e é um número válido
        if data.get("imc") is not None:
            try:
                imc = float(data["imc"])
                if imc > 30:
                    risk_score += 1
            except ValueError:
                print(f"Aviso: IMC inválido: {data['imc']}")
        
        # Verifica condições preexistentes
        if "hipertensao" in data.get("condicoes_preexistentes", []):
            risk_score += 2
        
        # Verifica histórico familiar
        if "preeclampsia_anterior" in data.get("historico_familiar", []):
            risk_score += 2
        
        # Determina o nível de risco
        if risk_score > 3:
            risk_level = "Alto"
        elif risk_score > 1:
            risk_level = "Moderado"
        else:
            risk_level = "Baixo"
        
        return {"risk_score": risk_score, "risk_level": risk_level}

    def calculate_gestational_diabetes_risk(self, data):
        risk_score = 0
        
        # Verifica se a idade está presente e é um número válido
        if data.get("idade") is not None:
            try:
                idade = int(data["idade"])
                if idade > 25:
                    risk_score += 1
            except ValueError:
                print(f"Aviso: Idade inválida: {data['idade']}")
        
        # Verifica se o IMC está presente e é um número válido
        if data.get("imc") is not None:
            try:
                imc = float(data["imc"])
                if imc > 25:
                    risk_score += 1
            except ValueError:
                print(f"Aviso: IMC inválido: {data['imc']}")
        
        # Verifica histórico familiar
        if "diabetes_gestacional_anterior" in data.get("historico_familiar", []):
            risk_score += 2
        if "diabetes_tipo2" in data.get("historico_familiar", []):
            risk_score += 1
        
        # Determina o nível de risco
        if risk_score > 3:
            risk_level = "Alto"
        elif risk_score > 1:
            risk_level = "Moderado"
        else:
            risk_level = "Baixo"
        
        return {"risk_score": risk_score, "risk_level": risk_level}
