from housing.entity.config_entity import ModelEvaluationConfig
from housing.entity.artifact_entity import ModelEvaluationArtifact
from housing.exception import HousingException
from housing.logger import logging
import os,sys

class ModelEvaluation:

    def __init__(self,
    model_evaluation_config:ModelEvaluationConfig):        
        try:
            logging.info(f"{'='*20}Model Evaluation log started.{'='*20}")
            self.model_evaluation_config= model_evaluation_config
            pass
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_model_evaluation(self)-> ModelEvaluationArtifact:
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e


    def __del__(self):
        logging.info(f"{'='*20}Model Evaluation log completed.{'='*20}")