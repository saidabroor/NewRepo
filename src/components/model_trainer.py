import os
import sys
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logging import logging
from src.utils import save_object, evaluate_model  

@dataclass
class ModelTrainingConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainingConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info('Data splitted')

            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            models = {
                'RandomForestRegressor': RandomForestRegressor(),
                'GradientBoostingRegressor': GradientBoostingRegressor(),
                'AdaBoostRegressor': AdaBoostRegressor(),
                'XGBRegressor': XGBRegressor(),
                'LinearRegressor': LinearRegression(),
                'DecisionTreeRegressor': DecisionTreeRegressor()
            }



            params = {
                'Decision Tree': {
                'criterion': ['squared_error', 'friedman_mse', 'absolute_eror', 'poisson']
                },
                'Random Forest': {
    'n_estimators': [8, 16, 32, 64, 128, 256]
},


'Gradient Boosting': {
'learning_rate': [0.1, 0.01, 0.05, 0.001],
'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
'n_estimators': [8, 16, 32, 64, 128, 256]
},
'Linear Regresion': {},
'XGBRegressor': {
'learning_rate': [0.1, 0.01, 0.05, 0.001],
'n_estimators': [8, 16, 32, 64, 128, 256]


},
'Adaboost Regressor': {
    'learning_rate': [0.1, 0.01, 0.05, 0.001],
'n_estimators': [8, 16, 32, 64, 128, 256]
},
}




            model_report, best_models = evaluate_model(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, models=models, params = params)
            best_model_score = max(model_report.values())
            best_model_name = [name for name, score in model_report.items() if score == best_model_score][0]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException('Yomon model: Tuning yoki boshqa model rivojlantirish metodi kerak.')

            logging.info(f'Best model found: {best_model_name} with score: {best_model_score}')

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(x_test)
            r2 = r2_score(y_test, predicted)

            return r2

        except Exception as e:
            raise CustomException(sys, e)