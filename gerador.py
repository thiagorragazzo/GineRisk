import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as file:
        file.write(content)

# Conteúdo dos arquivos
readme_content = """# GineRisk

GineRisk é um sistema avançado de automação para o preenchimento de calculadoras de risco ginecológico, utilizando processamento de linguagem natural em dados de anamnese digital.

## Desenvolvido por
Thiago Roque Ragazzo

## Contato
thiagoragazzo@gmail.com

## Instruções de Instalação e Uso
1. Clone o repositório
2. Instale as dependências com `pip install -r requirements.txt`
3. Execute `python src/api/endpoints.py` para iniciar o servidor
4. Acesse a interface web em `http://localhost:5000`
"""

ner_model_content = """from transformers import AutoTokenizer, AutoModelForTokenClassification
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
"""

risk_calculator_content = """class GynRiskCalculator:
    def calculate_preeclampsia_risk(self, data):
        risk_score = 0
        if data["idade"] > 35:
            risk_score += 1
        if data["imc"] > 30:
            risk_score += 1
        if "hipertensao" in data["condicoes_preexistentes"]:
            risk_score += 2
        if "preeclampsia_anterior" in data["historico_familiar"]:
            risk_score += 2
        
        risk_level = "Baixo"
        if risk_score > 3:
            risk_level = "Alto"
        elif risk_score > 1:
            risk_level = "Moderado"
        
        return {"risk_score": risk_score, "risk_level": risk_level}

    def calculate_gestational_diabetes_risk(self, data):
        risk_score = 0
        if data["idade"] > 25:
            risk_score += 1
        if data["imc"] > 25:
            risk_score += 1
        if "diabetes_gestacional_anterior" in data["historico_familiar"]:
            risk_score += 2
        if "diabetes_tipo2" in data["historico_familiar"]:
            risk_score += 1
        
        risk_level = "Baixo"
        if risk_score > 3:
            risk_level = "Alto"
        elif risk_score > 1:
            risk_level = "Moderado"
        
        return {"risk_score": risk_score, "risk_level": risk_level}
"""

data_processor_content = """import pandas as pd

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
"""

endpoints_content = """from flask import Flask, request, jsonify, render_template
from src.models.ner_model import BioBERTNERModel
from src.data.data_processor import DataProcessor
from src.models.risk_calculator import GynRiskCalculator
import logging

app = Flask(__name__, template_folder='../../templates')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ner_model = BioBERTNERModel()
data_processor = DataProcessor()
risk_calculator = GynRiskCalculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_anamnesis():
    logger.info("Recebida nova solicitação de processamento de anamnese")
    data = request.json
    text = data['text']
    
    entities = ner_model.extract_entities(text)
    structured_data = data_processor.structure_data(entities)
    preeclampsia_risk = risk_calculator.calculate_preeclampsia_risk(structured_data)
    gestational_diabetes_risk = risk_calculator.calculate_gestational_diabetes_risk(structured_data)
    
    logger.info(f"Processamento concluído. Risco de preeclampsia: {preeclampsia_risk['risk_level']}")
    
    return jsonify({
        "structured_data": structured_data,
        "risk_assessment": {
            "preeclampsia": preeclampsia_risk,
            "gestational_diabetes": gestational_diabetes_risk
        }
    })

@app.route('/feedback', methods=['POST'])
def receive_feedback():
    data = request.json
    logger.info(f"Feedback recebido: {data}")
    # Aqui você implementaria a lógica para armazenar e processar o feedback
    return jsonify({"status": "Feedback recebido com sucesso"})

if __name__ == '__main__':
    app.run(debug=True)
"""

index_html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GineRisk - Avaliação de Risco Ginecológico</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #2c3e50; }
        textarea { width: 100%; height: 150px; margin-bottom: 10px; }
        button { background-color: #3498db; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        button:hover { background-color: #2980b9; }
        #result { margin-top: 20px; border: 1px solid #ddd; padding: 10px; }
    </style>
</head>
<body>
    <h1>GineRisk - Avaliação de Risco Ginecológico</h1>
    <p>Desenvolvido por Thiago Roque Ragazzo</p>
    <textarea id="anamnesis" placeholder="Insira o texto da anamnese aqui..."></textarea>
    <button onclick="processAnamnesis()">Processar Anamnese</button>
    <div id="result"></div>

    <script>
        function processAnamnesis() {
            const anamnesis = document.getElementById('anamnesis').value;
            fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: anamnesis }),
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').innerHTML = `
                    <h2>Resultado da Análise</h2>
                    <h3>Dados Estruturados:</h3>
                    <pre>${JSON.stringify(data.structured_data, null, 2)}</pre>
                    <h3>Avaliação de Risco:</h3>
                    <pre>${JSON.stringify(data.risk_assessment, null, 2)}</pre>
                `;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
    </script>
</body>
</html>
"""

technical_doc_content = """# Documentação Técnica do GineRisk

## Visão Geral
O GineRisk é um sistema de avaliação de risco ginecológico desenvolvido por Thiago Roque Ragazzo. Utiliza processamento de linguagem natural para extrair informações relevantes de anamneses e calcular riscos específicos.

## Componentes Principais
1. Modelo NER (BioBERT-PT)
2. Processador de Dados
3. Calculadora de Risco
4. API RESTful
5. Interface de Usuário

## Fluxo de Dados
1. O texto da anamnese é enviado através da interface de usuário.
2. O modelo NER extrai entidades relevantes do texto.
3. O processador de dados estrutura as entidades extraídas.
4. A calculadora de risco avalia os dados estruturados.
5. Os resultados são retornados e exibidos na interface.

## Configuração e Execução
1. Clone o repositório: `git clone https://github.com/thiagorragazzo/GineRisk.git`
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o servidor: `python src/api/endpoints.py`
4. Acesse a interface web em `http://localhost:5000`

## Manutenção e Atualização
- Atualize regularmente as dependências do projeto.
- Realize fine-tuning periódico do modelo NER com novos dados.
- Mantenha as calculadoras de risco atualizadas com as últimas diretrizes médicas.
- Implemente um sistema de feedback para melhorias contínuas.

## Segurança e Conformidade
- Todos os dados são processados localmente para garantir a privacidade.
- Implemente medidas de segurança adicionais antes do uso em ambiente de produção.
- Certifique-se de estar em conformidade com as regulamentações de saúde locais.
"""

user_manual_content = """# Manual do Usuário do GineRisk para Ginecologistas

## Introdução
O GineRisk, desenvolvido por Thiago Roque Ragazzo, é uma ferramenta projetada para auxiliar ginecologistas na avaliação de riscos com base em anamneses de pacientes.

## Como Usar
1. Acesse a interface web do GineRisk em `http://localhost:5000`.
2. Insira o texto da anamnese no campo fornecido.
3. Clique no botão "Processar Anamnese".
4. Revise os resultados exibidos, incluindo dados estruturados e avaliações de risco.

## Interpretação dos Resultados
- Dados Estruturados: Mostra as informações extraídas da anamnese, como idade, peso, altura e histórico médico.
- Avaliação de Risco: Fornece pontuações e níveis de risco para condições específicas, como preeclampsia e diabetes gestacional.

## Limitações e Considerações
- O GineRisk é uma ferramenta de suporte à decisão e não substitui o julgamento clínico.
- Sempre verifique a precisão das informações extraídas.
- Considere fatores adicionais não capturados pela ferramenta.
- Use seu conhecimento e experiência clínica para interpretar os resultados no contexto de cada paciente.

## Suporte e Feedback
Para suporte ou feedback, entre em contato com Thiago Roque Ragazzo em thiagoragazzo@gmail.com.

## Atualizações e Melhorias
O GineRisk está em constante evolução. Fique atento a atualizações que podem incluir:
- Novos fatores de risco
- Melhorias na precisão da extração de informações
- Adição de novas calculadoras de risco

## Confidencialidade e Ética
- Assegure-se de obter o consentimento apropriado das pacientes antes de usar suas informações no sistema.
- Mantenha a confidencialidade dos dados das pacientes em todos os momentos.
- Use o GineRisk como um complemento, não um substituto, para a prática clínica ética e centrada no paciente.
"""

# Lista de arquivos a serem criados
files_to_create = [
    ('/Users/thiagoragazzo/GineRisk/README.md', readme_content),
    ('/Users/thiagoragazzo/GineRisk/src/models/ner_model.py', ner_model_content),
    ('/Users/thiagoragazzo/GineRisk/src/models/risk_calculator.py', risk_calculator_content),
    ('/Users/thiagoragazzo/GineRisk/src/data/data_processor.py', data_processor_content),
    ('/Users/thiagoragazzo/GineRisk/src/api/endpoints.py', endpoints_content),
    ('/Users/thiagoragazzo/GineRisk/templates/index.html', index_html_content),
    ('/Users/thiagoragazzo/GineRisk/docs/technical_documentation.md', technical_doc_content),
    ('/Users/thiagoragazzo/GineRisk/docs/user_manual.md', user_manual_content),
]

# Criar os arquivos
for file_path, content in files_to_create:
    create_file(file_path, content)

print("Todos os arquivos foram criados com sucesso!")
