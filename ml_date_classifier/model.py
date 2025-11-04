import joblib
from pathlib import Path


def load_model(p='models/model.joblib'):
    return joblib.load(Path(p))


def predict(model, texts):
    vect = model['vect']
    clf = model['clf']
    X = vect.transform(texts)
    preds = clf.predict(X)
    return preds