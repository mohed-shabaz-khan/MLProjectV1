from fastapi import FastAPI
from pydantic import BaseModel
from ml_date_classifier.model import load_model, predict


app = FastAPI()
model = None


class Request(BaseModel):
    texts: list[str]


@app.on_event('startup')
def load():
    global model
    model = load_model()


@app.post('/predict')
def predict_route(req: Request):
    preds = predict(model, req.texts)
    return {'predictions': preds.tolist()}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)