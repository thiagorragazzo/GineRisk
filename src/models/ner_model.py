from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

class NERModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('emilyalsentzer/Bio_ClinicalBERT')
        self.model = AutoModelForTokenClassification.from_pretrained('emilyalsentzer/Bio_ClinicalBERT')
        self.model.eval()

    def extract_entities(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        predictions = torch.argmax(outputs.logits, dim=2)
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        
        entities = {}
        current_entity = None
        current_tokens = []

        for token, pred in zip(tokens, predictions[0]):
            if pred != 0:  # 0 is typically the 'O' (Outside) label
                label = self.model.config.id2label[pred.item()]
                if label != current_entity:
                    if current_entity:
                        entities.setdefault(current_entity, []).append(" ".join(current_tokens))
                        current_tokens = []
                    current_entity = label
                current_tokens.append(token)
            elif current_entity:
                entities.setdefault(current_entity, []).append(" ".join(current_tokens))
                current_entity = None
                current_tokens = []

        if current_entity:
            entities.setdefault(current_entity, []).append(" ".join(current_tokens))

        return self.post_process_entities(entities)

    def post_process_entities(self, entities):
        processed = {}
        for key, values in entities.items():
            if key == 'AGE':
                processed['age'] = int(''.join(filter(str.isdigit, values[0])))
            elif key == 'BMI':
                processed['bmi'] = float(values[0])
            elif key == 'BLOOD_PRESSURE':
                processed['blood_pressure'] = values[0]
            elif key == 'FAMILY_HISTORY':
                processed['family_history'] = values
            # Add more entity processing as needed
        return processed