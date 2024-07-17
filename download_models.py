import sys
from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSeq2SeqLM, AutoModelForMaskedLM

def download_model(model_name, model_class):
    print(f"Baixando {model_name}...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = model_class.from_pretrained(model_name)
        print(f"{model_name} baixado com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar {model_name}: {str(e)}")
        print("Tentando continuar com os próximos modelos...")

models = [
    ("xlm-roberta-large", AutoModelForTokenClassification),
    ("microsoft/BioGPT", AutoModelForSeq2SeqLM),
    ("emilyalsentzer/Bio_ClinicalBERT", AutoModelForTokenClassification),
    ("dmis-lab/biobert-base-cased-v1.1", AutoModelForMaskedLM),
    ("monologg/biobert_v1.1_pubmed", AutoModelForTokenClassification)
]

print("Iniciando o download dos modelos...")
for model_name, model_class in models:
    download_model(model_name, model_class)

print("Processo de download concluído!")
