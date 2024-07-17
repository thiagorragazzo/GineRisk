from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

class BioBERTNERModel:
    def __init__(self, model_name="pucpr/biobertpt-all"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.model.eval()

    def extract_entities(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=2)
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        
        entities = []
        current_entity = None
        for token, pred in zip(tokens, predictions[0]):
            if pred != 0:  # 0 is typically the 'O' (Outside) label
                if current_entity is None:
                    current_entity = {"type": self.model.config.id2label[pred.item()], "text": token}
                else:
                    current_entity["text"] += f" {token}"
            elif current_entity:
                entities.append(current_entity)
                current_entity = None
        
        if current_entity:
            entities.append(current_entity)
        
        return entities
