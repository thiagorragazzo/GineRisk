from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSeq2SeqLM, AutoModelForMaskedLM
import torch
import re

class MultiModelNER:
    def __init__(self):
        self.models = {
            'xlm-roberta': self.load_model('xlm-roberta-large', AutoModelForTokenClassification),
            'biogpt': self.load_model('microsoft/BioGPT', AutoModelForSeq2SeqLM),
            'clinicalbert': self.load_model('emilyalsentzer/Bio_ClinicalBERT', AutoModelForTokenClassification),
            'biobert': self.load_model('dmis-lab/biobert-base-cased-v1.1', AutoModelForMaskedLM),
            'bert-biomed': self.load_model('monologg/biobert_v1.1_pubmed', AutoModelForTokenClassification)
        }

    def load_model(self, model_name, model_class):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = model_class.from_pretrained(model_name)
        model.eval()
        return {'tokenizer': tokenizer, 'model': model}

    def extract_entities(self, text):
        results = {}
        for model_name, model_data in self.models.items():
            results[model_name] = self.process_with_model(text, model_data)
        return results

    def process_with_model(self, text, model_data):
        tokenizer = model_data['tokenizer']
        model = model_data['model']

        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)

        # Process outputs based on model type
        if isinstance(model, AutoModelForTokenClassification):
            return self.process_token_classification(tokenizer, inputs, outputs)
        elif isinstance(model, AutoModelForSeq2SeqLM):
            return self.process_seq2seq(tokenizer, outputs)
        elif isinstance(model, AutoModelForMaskedLM):
            return self.process_masked_lm(tokenizer, inputs, outputs)

    def process_token_classification(self, tokenizer, inputs, outputs):
        predictions = torch.argmax(outputs.logits, dim=2)
        tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        
        entities = {}
        current_entity = None
        current_tokens = []

        for token, pred in zip(tokens, predictions[0]):
            if pred != 0:  # 0 is typically the 'O' (Outside) label
                entity_type = self.model.config.id2label[pred.item()]
                if entity_type != current_entity:
                    if current_entity:
                        entity_value = " ".join(current_tokens).replace(" ##", "")
                        entities.setdefault(current_entity, []).append(entity_value)
                        current_tokens = []
                    current_entity = entity_type
                current_tokens.append(token)
            elif current_entity:
                entity_value = " ".join(current_tokens).replace(" ##", "")
                entities.setdefault(current_entity, []).append(entity_value)
                current_entity = None
                current_tokens = []
        
        if current_entity:
            entity_value = " ".join(current_tokens).replace(" ##", "")
            entities.setdefault(current_entity, []).append(entity_value)

        return entities

    def process_seq2seq(self, tokenizer, outputs):
        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Here you might need to implement custom logic to extract entities from the generated text
        return {'generated_text': generated}

    def process_masked_lm(self, tokenizer, inputs, outputs):
        mask_token_index = torch.where(inputs["input_ids"] == tokenizer.mask_token_id)[1]
        mask_token_logits = outputs.logits[0, mask_token_index, :]
        top_5_tokens = torch.topk(mask_token_logits, 5, dim=1).indices[0].tolist()
        
        return {'top_predictions': [tokenizer.decode([token_id]) for token_id in top_5_tokens]}

    def rule_based_extraction(self, text):
        entities = {}
        
        age_match = re.search(r'(\d+)\s*anos', text)
        if age_match:
            entities['idade'] = int(age_match.group(1))
        
        weight_match = re.search(r'(\d+(?:\.\d+)?)\s*kg', text)
        if weight_match:
            entities['peso'] = float(weight_match.group(1))
        
        height_match = re.search(r'(\d+(?:\.\d+)?)\s*cm', text)
        if height_match:
            entities['altura'] = float(height_match.group(1))
        
        if 'hipertensão crônica' in text.lower():
            entities['condicoes_preexistentes'] = ['hipertensão crônica']
        
        if 'preeclampsia durante a gravidez' in text.lower():
            entities['historico_familiar'] = ['preeclampsia']
        
        return entities
