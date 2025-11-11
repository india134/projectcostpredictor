from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
import mlflow
import time
from datetime import datetime

mlflow.set_tracking_uri("file:///app/mlruns")   # Store logs locally inside container
mlflow.set_experiment("iris_deployment_tracking")

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

from datetime import datetime
import time
import mlflow

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request,
                  sepal_length: float = Form(...),
                  sepal_width: float = Form(...),
                  petal_length: float = Form(...),
                  petal_width: float = Form(...)):

    # Start timer for latency tracking
    start_time = time.time()

    try:
        # Prepare features
        X = [[sepal_length, sepal_width, petal_length, petal_width]]
        prediction = model.predict(X)[0]
        flower = target_names[prediction]

        # End timer
        latency = round(time.time() - start_time, 3)

        # --- MLflow logging section ---
        mlflow.set_tracking_uri("file:///app/mlruns")  # local tracking directory
        mlflow.set_experiment("iris_deployment_tracking")

        with mlflow.start_run(run_name="inference_run", nested=True):
            mlflow.log_param("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            mlflow.log_param("sepal_length", sepal_length)
            mlflow.log_param("sepal_width", sepal_width)
            mlflow.log_param("petal_length", petal_length)
            mlflow.log_param("petal_width", petal_width)
            mlflow.log_metric("latency_sec", latency)
            mlflow.log_param("prediction", flower)

        # Return same template response (frontend stays same)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": flower
        })

    except Exception as e:
        # Log the error in MLflow
        mlflow.set_experiment("iris_deployment_tracking")
        with mlflow.start_run(run_name="error_run", nested=True):
            mlflow.log_param("error", str(e))
            mlflow.log_param("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Return an error response on the web page
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": f"Error: {str(e)}"
        })
