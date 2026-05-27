import streamlit as st
import requests
import plotly.express as px
import pandas as pd
st.set_page_config(page_title="AI Loan Risk Prediction", layout="wide")

st.title("🏦 AI Loan Risk Prediction System")

st.markdown("### Fintech AI Application using XGBoost + FastAPI + Streamlit")

# Create 2 columns
col1, col2 = st.columns(2)

# Left Column
with col1:

    gender = st.selectbox("Gender", [0, 1])

    married = st.selectbox("Married", [0, 1])

    dependents = st.selectbox("Dependents", [0, 1, 2, 3])

    education = st.selectbox("Education", [0, 1])

    self_employed = st.selectbox("Self Employed", [0, 1])

    income = st.number_input("Applicant Income")

# Right Column
with col2:

    co_income = st.number_input("Coapplicant Income")

    loan_amount = st.number_input("Loan Amount")

    loan_term = st.number_input("Loan Amount Term")

    credit_history = st.selectbox("Credit History", [0, 1])

    property_area = st.selectbox("Property Area", [0, 1, 2])

# Predict Button
if st.button("Predict Loan Status"):

    data = {
        "Gender": gender,
        "Married": married,
        "Dependents": dependents,
        "Education": education,
        "Self_Employed": self_employed,
        "ApplicantIncome": income,
        "CoapplicantIncome": co_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_term,
        "Credit_History": credit_history,
        "Property_Area": property_area
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=data
    )

    result = response.json()

    prediction = result["Loan Prediction"]

    if prediction == "Approved":
        st.success(f"✅ Loan Status: {prediction}")
    else:
        st.error(f"❌ Loan Status: {prediction}")

    if "Approval Probability" in result:
        st.info(f"Approval Probability: {result['Approval Probability']}%")
        st.markdown("---")

st.subheader("📊 Loan Risk Analytics")

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
