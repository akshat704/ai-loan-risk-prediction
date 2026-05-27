from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

model = joblib.load("models/risk_model.pkl")

class LoanData(BaseModel):

    Gender: int
    Married: int
    Dependents: int
    Education: int
    Self_Employed: int
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: int


@app.get("/")
def home():

    return {"message": "Loan Risk API Running"}


@app.post("/predict")
def predict(data: LoanData):

    input_data = pd.DataFrame([{
        "Gender": data.Gender,
        "Married": data.Married,
        "Dependents": data.Dependents,
        "Education": data.Education,
        "Self_Employed": data.Self_Employed,
        "ApplicantIncome": data.ApplicantIncome,
        "CoapplicantIncome": data.CoapplicantIncome,
        "LoanAmount": data.LoanAmount,
        "Loan_Amount_Term": data.Loan_Amount_Term,
        "Credit_History": data.Credit_History,
        "Property_Area": data.Property_Area
    }])

    prediction = model.predict(input_data)

    probability = model.predict_proba(input_data)[0][1]

    result = "Approved" if prediction[0] == 1 else "Rejected"

    return {
        "Loan Prediction": result,
        "Approval Probability": round(probability * 100, 2)
    }