import os
import sys
import numpy as np
import pandas as pd
import dill
import pickle

from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logging import logging

from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
  try:
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, 'wb') as file_obj:
      dill.dump(obj, file_obj)
  except Exception as e:
    raise CustomException(e, sys)
  
def evaluate_model(x_train, y_train, x_test, y_test, models, params=params):
  try:
    report = {}
    best_model = {}


    for model_name, model in models.items():
      logging.info('Grid serach cv has started.')

      model_param = params.get(model_name, None)

      if model_param:
        gs = GridSearchCV(model, model_param, cv=3, n_jobs=-1, verbose=0)
        gs.fit(x_train, y_train)
        best_model = gs.best_estimator_

      else:
        model.fit(x_train, y_train)
        best_model = model

      y_test_pred = best_model.predict(x_test)
      test_model_score = r2_score(y_test, y_test_pred)


      report[model_name] = test_model_score
      best_model[model_name] = best_model
      logging.info('Best model found.')

    return report, best_model

  except Exception as e:
    raise CustomException(e, sys)


aaaaaaaaaaaaaaaaafgggggggg