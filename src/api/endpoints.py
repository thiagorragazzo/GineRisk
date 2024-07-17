from flask import Flask, request, jsonify, render_template
from ..data.data_processor import DataProcessor
from ..models.risk_calculator import GynRiskCalculator
import logging

app = Flask(__name__, template_folder='../../templates')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    
    try:
        structured_data = data_processor.structure_data(text)
        risk_assessments = {}
        
        for model, model_data in structured_data.items():
            preeclampsia_risk = risk_calculator.calculate_preeclampsia_risk(model_data)
            gestational_diabetes_risk = risk_calculator.calculate_gestational_diabetes_risk(model_data)
            risk_assessments[model] = {
                "preeclampsia": preeclampsia_risk,
                "gestational_diabetes": gestational_diabetes_risk
            }
        
        logger.info(f"Dados estruturados: {structured_data}")
        logger.info(f"Avaliações de risco: {risk_assessments}")
        
        return jsonify({
            "structured_data": structured_data,
            "risk_assessments": risk_assessments
        })
    except Exception as e:
        logger.error(f"Erro durante o processamento: {str(e)}")
        return jsonify({"error": "Ocorreu um erro durante o processamento da anamnese"}), 500

@app.route('/feedback', methods=['POST'])
def receive_feedback():
    data = request.json
    logger.info(f"Feedback recebido: {data}")
    # Aqui você implementaria a lógica para armazenar e processar o feedback
    return jsonify({"status": "Feedback recebido com sucesso"})

if __name__ == '__main__':
    app.run(debug=True)
