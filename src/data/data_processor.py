from src.models.ner_model import MultiModelNER

class DataProcessor:
    def __init__(self):
        self.ner_model = MultiModelNER()

    def structure_data(self, text):
        entities = self.ner_model.extract_entities(text)
        rule_based_entities = self.ner_model.rule_based_extraction(text)
        
        structured_data = {model: self.process_model_entities(model_entities, rule_based_entities) 
                           for model, model_entities in entities.items()}
        
        return structured_data

    def process_model_entities(self, model_entities, rule_based_entities):
        processed_data = {
            "idade": rule_based_entities.get("idade"),
            "peso": rule_based_entities.get("peso"),
            "altura": rule_based_entities.get("altura"),
            "imc": None,
            "pressao_arterial": None,
            "historico_familiar": rule_based_entities.get("historico_familiar", []),
            "condicoes_preexistentes": rule_based_entities.get("condicoes_preexistentes", []),
            "medicacoes": [],
        }
        
        # Add model-specific entities
        for entity_type, values in model_entities.items():
            if entity_type.lower() in processed_data:
                processed_data[entity_type.lower()] = values[0] if values else None
        
        if processed_data["peso"] and processed_data["altura"]:
            processed_data["imc"] = processed_data["peso"] / ((processed_data["altura"] / 100) ** 2)
        
        return processed_data
