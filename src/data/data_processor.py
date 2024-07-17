from src.models.ner_model import NERModel
from src.utils.risk_calculator import calculate_risks
from src.utils.text_generator import generate_explanation
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self.ner_model = NERModel()

    def process(self, anamnesis, risk_type):
        logger.info(f"Processing anamnesis for risk type: {risk_type}")
        entities = self.ner_model.extract_entities(anamnesis)
        logger.debug(f"Extracted entities: {entities}")
        risks = calculate_risks(entities, risk_type)
        logger.debug(f"Calculated risks: {risks}")
        explanation = generate_explanation(risks, anamnesis, risk_type)
        logger.debug(f"Generated explanation: {explanation}")
        return {"risks": risks, "explanation": explanation}