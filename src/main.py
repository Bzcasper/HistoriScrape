from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI-Integrated API is running."}

@app.post("/train-model")
def train_model(data: dict):
    # Placeholder for model training logic
    return {"message": "Model training initiated."}
