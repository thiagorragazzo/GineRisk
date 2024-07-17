from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class BioGPTGenerator:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/biogpt")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/biogpt")

    def generate_explanation(self, results, anamnesis, risk_type):
        prompt = f"Based on the anamnesis, the calculated risk for {risk_type} is {results['risk']}. Explain this result:"
        
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=200,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True
            )
        
        explanation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return explanation

generator = BioGPTGenerator()

def generate_explanation(results, anamnesis, risk_type):
    return generator.generate_explanation(results, anamnesis, risk_type)