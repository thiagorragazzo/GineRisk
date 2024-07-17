from flask import Flask, request, jsonify, render_template
from src.data.data_processor import DataProcessor
import logging

app = Flask(__name__, template_folder='/Users/thiagoragazzo/GineRisk/templates')
data_processor = DataProcessor()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_anamnesis():
    try:
        data = request.json
        logger.debug(f"Received data: {data}")
        anamnesis = data['anamnesis']
        risk_type = data['risk_type']
        logger.info(f"Processing anamnesis for risk type: {risk_type}")
        results = data_processor.process(anamnesis, risk_type)
        logger.debug(f"Processing results: {results}")
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error processing anamnesis: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)