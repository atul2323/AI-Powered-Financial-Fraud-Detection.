import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import os
# Load model and feature names
model = joblib.load("faud_detection.pkl")
feature_names = joblib.load("feature_names.pkl")

st.title("💳 AI-Powered Financial Fraud Detection")

st.write("Enter transaction details below")

# User Inputs
amount = st.number_input("Amount", min_value=0.0)

transaction_type = st.selectbox(
    "Transaction Type",
    ["ATM", "POS", "Online", "QR"]
)

merchant_category = st.selectbox(
    "Merchant Category",
    [
        "Food",
        "Travel",
        "Electronics",
        "Grocery"
    ]
)
country = st.selectbox(
    "Country",
    ["US", "UK", "FR", "NG", "TR"]
)

hour = st.slider(
    "Transaction Hour",
    0,
    23,
    12
)

# Auto-generated risk scores
risk_profile = st.selectbox(
    "Risk Profile",
    [
        "Low Risk",
        "Medium Risk",
        "High Risk"
    ]
)

if risk_profile == "Low Risk":
    device_risk_score = 0.15
    ip_risk_score = 0.10

elif risk_profile == "Medium Risk":
    device_risk_score = 0.50
    ip_risk_score = 0.45

else:
    device_risk_score = 0.95
    ip_risk_score = 0.90
if st.button("Predict Fraud"):

    # Create input dictionary
    input_data = {}

    # Initialize all features to 0
    for col in feature_names:
        input_data[col] = 0

    # Numerical Features
    if "amount" in feature_names:
        input_data["amount"] = amount

    if "hour" in feature_names:
        input_data["hour"] = hour

    if "device_risk_score" in feature_names:
        input_data["device_risk_score"] = device_risk_score

    if "ip_risk_score" in feature_names:
        input_data["ip_risk_score"] = ip_risk_score

    # Dummy Columns
    transaction_col = f"transaction_type_{transaction_type}"
    merchant_col = f"merchant_category_{merchant_category}"
    country_col = f"country_{country}"

    if transaction_col in feature_names:
        input_data[transaction_col] = 1

    if merchant_col in feature_names:
        input_data[merchant_col] = 1

    if country_col in feature_names:
        input_data[country_col] = 1

    # Create dataframe
    input_df = pd.DataFrame([input_data])

    # Prediction
    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0][1]

    # Display result
    if prediction == 1:
        st.error(
            f"⚠️ Fraud Detected\n\nProbability: {probability:.2%}"
        )
    else:
        st.success(
            f"✅ Legitimate Transaction\n\nProbability: {probability:.2%}"
        )

    # Save to Excel
    record = pd.DataFrame([{
        "Date": datetime.now(),
        "Amount": amount,
        "Transaction_Type": transaction_type,
        "Merchant_Category": merchant_category,
        "Country": country,
        "Hour": hour,
        "Device_Risk_Score": device_risk_score,
        "IP_Risk_Score": ip_risk_score,
        "Prediction": "Fraud" if prediction == 1 else "Not Fraud"
    }])

    excel_file = "transactions.xlsx"

    if os.path.exists(excel_file):
        old = pd.read_excel(excel_file)
        new = pd.concat([old, record], ignore_index=True)
        new.to_excel(excel_file, index=False)
    else:
        record.to_excel(excel_file, index=False)

    st.write("Transaction saved to Excel.")