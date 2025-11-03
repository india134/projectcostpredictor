from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib

# Initialize app
app = FastAPI(title="Iris Classifier")

# Load model
model = joblib.load("model.pkl")
target_names = ['Setosa', 'Versicolor', 'Virginica']

# Templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request,
                  sepal_length: float = Form(...),
                  sepal_width: float = Form(...),
                  petal_length: float = Form(...),
                  petal_width: float = Form(...)):

    X = [[sepal_length, sepal_width, petal_length, petal_width]]
    prediction = model.predict(X)[0]
    flower = target_names[prediction]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": flower
    })

