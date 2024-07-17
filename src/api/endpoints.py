from flask import Flask, request, jsonify, render_template
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
