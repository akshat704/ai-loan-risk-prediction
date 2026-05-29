from fastapi import FastAPI
import joblib
import numpy as np

# Create FastAPI app
app = FastAPI()

# Load trained model
model = joblib.load("models/risk_model.pkl")


# Home Route
@app.get("/")
def home():
    return {
        "message": "AI Loan Risk Prediction API Running"
    }


# Prediction Route
@app.post("/predict")
def predict(
    Gender: int,
    Married: int,
    Dependents: int,
    Education: int,
    Self_Employed: int,
    ApplicantIncome: float,
    CoapplicantIncome: float,
    LoanAmount: float,
    Loan_Amount_Term: float,
    Credit_History: int,
    Property_Area: int
):

    # Create input array
    data = np.array([[
        Gender,
        Married,
        Dependents,
        Education,
        Self_Employed,
        ApplicantIncome,
        CoapplicantIncome,
        LoanAmount,
        Loan_Amount_Term,
        Credit_History,
        Property_Area
    ]])

    # Make prediction
    prediction = int(model.predict(data)[0])

    # Prediction probability
    probability = float(
        model.predict_proba(data)[0][1]
    )

    # Convert prediction to text
    if prediction == 1:
        result = "Approved"
    else:
        result = "Rejected"

    # Return JSON response
    return {
        "Loan Prediction": result,
        "Probability": round(probability * 100, 2)
    }