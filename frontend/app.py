import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Page Title
st.title("🏦 AI Loan Risk Prediction System")

st.write("Enter Applicant Details")

# Input Fields
Gender = st.selectbox("Gender", [0, 1])

Married = st.selectbox("Married", [0, 1])

Dependents = st.selectbox("Dependents", [0, 1, 2, 3])

Education = st.selectbox("Education", [0, 1])

Self_Employed = st.selectbox("Self Employed", [0, 1])

ApplicantIncome = st.number_input(
    "Applicant Income",
    value=5000
)

CoapplicantIncome = st.number_input(
    "Coapplicant Income",
    value=2000
)

LoanAmount = st.number_input(
    "Loan Amount",
    value=120
)

Loan_Amount_Term = st.number_input(
    "Loan Amount Term",
    value=360
)

Credit_History = st.selectbox(
    "Credit History",
    [0, 1]
)

Property_Area = st.selectbox(
    "Property Area",
    [0, 1, 2]
)

# Prediction Button
if st.button("Predict Loan Status"):

    try:

        # Send Request To Backend
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            params={
                "Gender": Gender,
                "Married": Married,
                "Dependents": Dependents,
                "Education": Education,
                "Self_Employed": Self_Employed,
                "ApplicantIncome": ApplicantIncome,
                "CoapplicantIncome": CoapplicantIncome,
                "LoanAmount": LoanAmount,
                "Loan_Amount_Term": Loan_Amount_Term,
                "Credit_History": Credit_History,
                "Property_Area": Property_Area
            }
        )

        # Convert Response To JSON
        result = response.json()


        # Get Prediction
        prediction = result.get(
            "Loan Prediction",
            "No Prediction Returned"
        )

        # Get Probability
        probability = result.get(
            "Probability",
            0
        )

        # Show Output
        st.success(f"Loan Status: {prediction}")

        st.info(
            f"Approval Probability: {probability}%"
        )

    except Exception as e:

        st.error(f"Error: {e}")

# Analytics Section
st.markdown("---")

st.subheader("📊 Loan Analytics Dashboard")

chart_data = pd.DataFrame({
    "Category": ["Approved", "Rejected"],
    "Count": [80, 20]
})

fig = px.bar(
    chart_data,
    x="Category",
    y="Count",
    title="Loan Approval Distribution"
)

st.plotly_chart(fig)
