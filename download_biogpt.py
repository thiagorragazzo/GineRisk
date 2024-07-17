from transformers import AutoTokenizer, AutoModelForCausalLM

def download_biogpt():
    try:
        print("Baixando microsoft/BioGPT...")
        tokenizer = AutoTokenizer.from_pretrained('microsoft/BioGPT')
        model = AutoModelForCausalLM.from_pretrained('microsoft/BioGPT')
        print("microsoft/BioGPT baixado com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar microsoft/BioGPT: {e}")

if __name__ == "__main__":
    download_biogpt()
