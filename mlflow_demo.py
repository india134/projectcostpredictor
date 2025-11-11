import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
acc = model.score(X_test, y_test)

# ---- MLflow Tracking ----
mlflow.start_run()
mlflow.log_param("model", "RandomForest")
mlflow.log_param("n_estimators", 100)
mlflow.log_metric("accuracy", acc)
mlflow.sklearn.log_model(model, "model")
mlflow.end_run()
