from transformers import AutoTokenizer, AutoModelForTokenClassification

model_name = "pucpr/biobertpt-all"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

print("Modelo baixado com sucesso!")
