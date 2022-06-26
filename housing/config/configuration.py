from curses import raw
import os,sys
from housing.entity.config_entity import *
from housing.exception import HousingException
from housing.util.util import  read_yaml_file
from housing.constant import *
from housing.exception import HousingException
from housing.logger import logging


class Configuration:
    def __init__(self,
        config_file_path:str =CONFIG_FILE_PATH,
        schema_file_path:str = SCHEMA_FILE_PATH,
        current_time_stamp:str = CURRENT_TIME_STAMP
        ) -> None:
        try:
            self.config_info  = read_yaml_file(file_path=config_file_path)
            self.schema_info = read_yaml_file(file_path=schema_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise HousingException(e,sys) from e


    def get_data_ingestion_config(self) ->DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir=os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
            )
            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
            
            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]
            tgz_download_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY]
            )
            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )

            ingested_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
            )
            ingested_train_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )
            ingested_test_dir =os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
            )


            data_ingestion_config=DataIngestionConfig(
                dataset_download_url=dataset_download_url, 
                tgz_download_dir=tgz_download_dir, 
                raw_data_dir=raw_data_dir, 
                ingested_train_dir=ingested_train_dir, 
                ingested_test_dir=ingested_test_dir
            )
            logging.info(f"Data Ingestion config: {data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_validation_config(self)->DataValidationConfig:
        try:
            data_validation_info = self.config_info[DATA_VALIDATION_CONFIG_KEY]
            schema_file_path = data_validation_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
            data_validation_config = DataValidationConfig(schema_file_path=schema_file_path)
            logging.info(f"Data Validation config: {data_validation_config}")
            return data_validation_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_transformation_config(self)-> DataTransformationConfig:
        try:
            data_transformation_config = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]
            schema_file_path = data_validation_config[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
            data_validation_config = DataValidationConfig(schema_file_path=schema_file_path)
            logging.info(f"Data Transformation config: {data_transformation_config}")
            return data_transformation_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_model_trainer_config(self)-> ModelTrainerConfig:
        pass

    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        try:
            model_evaluation_config = self.config_info[MODEL_PUSHER_CONFIG_KEY]
            export_dir_path = model_evaluation_config[MODEL_PUSHER_EXPORT_DIR_KEY]
            model_evaluation_config = ModelPusherConfig(export_dir_path=export_dir_path)
            logging.info(f"Data Transformation config: {model_evaluation_config}")
            return model_evaluation_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_model_pusher_config(self)->ModelPusherConfig:
        try:
            model_pusher_config = self.config_info[MODEL_PUSHER_CONFIG_KEY]
            artifact_dir = self.training_pipeline_config.artifact_dir
            export_dir_path = os.path.join(artifact_dir,
            model_pusher_config[MODEL_PUSHER_EXPORT_DIR_KEY],
            self.time_stamp
            )
            model_pusher_config = ModelPusherConfig(export_dir_path=export_dir_path)
            logging.info(f"Data Transformation config: {model_pusher_config}")
            return model_pusher_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]        
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )

            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipeline config:{training_pipeline_config}")
            return training_pipeline_config

        except Exception as e:
            raise HousingException(e,sys) from e