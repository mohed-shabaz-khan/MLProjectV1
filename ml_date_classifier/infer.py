# ---------------------------------------------------------
# 📘 infer.py — FastAPI Inference API for ML Date Classifier
# ---------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel
from ml_date_classifier.model import load_model, predict

app = FastAPI(title="ML Date Classifier API", version="1.0")
model = None


# 🧩 Request Schema
class Request(BaseModel):
    texts: list[str]


# 🚀 Load model at startup
@app.on_event("startup")
def load():
    global model
    model = load_model()


# 🧠 Predict endpoint
@app.post("/predict")
def predict_route(req: Request):
    preds = predict(model, req.texts)
    return {"predictions": preds.tolist()}


# 🩺 Health check endpoint for monitoring & Jenkins validation
@app.get("/health")
def health():
    return {"status": "ok"}


# 🔥 Run app when executed directly (Docker will use CMD instead)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
