import joblib, json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


MODEL_PATH = Path('models')


def train(processed_json='data/processed/processed.json'):
    data = json.loads(Path(processed_json).read_text())
    texts = [d['text'] for d in data]
    y = [min(2, len(d['dates'])) for d in data] # labels: 0,1,2+
    vect = TfidfVectorizer(ngram_range=(1,2), max_features=1000)
    X = vect.fit_transform(texts)
    clf = LogisticRegression(max_iter=500)
    clf.fit(X, y)
    MODEL_PATH.mkdir(parents=True, exist_ok=True)
    joblib.dump({'vect': vect, 'clf': clf}, MODEL_PATH / 'model.joblib')
    print('✅ Model trained and saved to models/model.joblib')


if __name__ == '__main__':
    train()