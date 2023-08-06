import pickle
import math
import numpy as np
from sklearn.externals import joblib


def Scaler(format):
    scaler = joblib.load('scalers/%s.pkl'%(format))
    return scaler

def Model(format):
    model = joblib.load('models/%s.pkl'%(format))
    return model

def Predict(format,run,wickets,over,striker,non_striker):
    scaler = Scaler(format)
    model = Model(format)
    predict_score = model.predict(scaler.transform(np.array([[run,wickets,over,striker,non_striker]])))
    return math.ceil(predict_score[0])

