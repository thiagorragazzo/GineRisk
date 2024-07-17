import pandas as pd

class DataProcessor:
    def structure_data(self, entities):
        structured_data = {
            "idade": None,
            "peso": None,
            "altura": None,
            "imc": None,
            "pressao_arterial": None,
            "historico_familiar": [],
            "condicoes_preexistentes": [],
            "medicacoes": [],
        }
        
        for entity in entities:
            if entity["type"] == "AGE":
                structured_data["idade"] = int(entity["text"])
            elif entity["type"] == "WEIGHT":
                structured_data["peso"] = float(entity["text"].split()[0])
            elif entity["type"] == "HEIGHT":
                structured_data["altura"] = float(entity["text"].split()[0])
            # Adicione mais mapeamentos conforme necessário
        
        if structured_data["peso"] and structured_data["altura"]:
            structured_data["imc"] = structured_data["peso"] / ((structured_data["altura"] / 100) ** 2)
        
        return structured_data
