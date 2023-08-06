import json
import os

from joblib import dump
import matplotlib.pyplot as plt
import numpy as np
from sacred import Experiment
from sklearn import ensemble
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error

from sacred_integration import NeptuneObserver

ex = Experiment("train_experiment")
ex.observers.append(NeptuneObserver(project_name='jakub-czakon/contrib'))

@ex.config
def config():
    MODEL_DIR = 'sacred_models'
    MODEL_FILE = 'model.pkl'
    # Path to persist serialized model object
    MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)
    # Hyperparmater settings for GradientBoostedRegressor
    params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2,

              'learning_rate': 0.01, 'loss': 'ls'}

@ex.automain
def train_model(MODEL_DIR, MODEL_FILE, MODEL_PATH, params):
    # ##########################################################################
    # Load data
    print("Loading data...")
    boston = datasets.load_boston()

    print("Splitting data...")
    X, y = shuffle(boston.data, boston.target, random_state=13)
    X = X.astype(np.float32)
    offset = int(X.shape[0] * 0.9)
    X_train, y_train = X[:offset], y[:offset]
    X_test, y_test = X[offset:], y[offset:]

    # ##########################################################################
    # Fit regression model
    print("Fitting model...")
    clf = ensemble.GradientBoostingRegressor(**params)
    clf.fit(X_train, y_train)

    train_mse = mean_squared_error(y_train, clf.predict(X_train))
    test_mse = mean_squared_error(y_test, clf.predict(X_test))

    print("Serializing model to: {}".format(MODEL_PATH))
    dump(clf, MODEL_PATH)

    ex.log_scalar("training.mean_square_error", train_mse)
    ex.log_scalar("testing.mean_square_error", test_mse)

    ex.add_artifact(MODEL_PATH)