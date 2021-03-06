import numpy as np
import pandas as pd
from utils.config import Config
import os

from scipy.stats import rankdata


def blend_predictions(predict_list, one_prediction, blend_name):
    print("Rank averaging on ", len(predict_list), " files")
    predictions = np.zeros_like(predict_list[0])
    for predict in predict_list:
        for i in range(1):
            predictions[:, i] = np.add(predictions[:, i], rankdata(predict[:, i])/predictions.shape[0])
    predictions /= len(predict_list)

    one_prediction["HasDetections"] = predictions
    one_prediction.to_csv('%s.csv' % blend_name, index=False)
    one_prediction.to_csv('%s.csv.zip' % blend_name, index=False, compression='zip')


if __name__ == '__main__':
    LABELS = ["HasDetections"]
    predict_list = []
    one_prediction = None
    blend_name = ''
    for file in os.listdir('data/blend'):
        filepath = 'data/blend/' + file
        one_prediction = pd.read_csv(filepath)
        predict_list.append(one_prediction[LABELS].values)
        blend_name += file.split('.')[0]
        blend_name += '--'

    blend_predictions(predict_list, one_prediction, blend_name)
