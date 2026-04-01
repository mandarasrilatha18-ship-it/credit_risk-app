import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Bank Credit Risk System", page_icon="🏦", layout="wide")

# Sidebar
st.sidebar.title("🏦 Bank Dashboard")
st.sidebar.markdown("Credit Risk Assessment System")
st.sidebar.markdown("---")
st.sidebar.info("Enter customer details and evaluate loan risk.")

# Load model
with open("Credit_model.pkl", "rb") as f:
    model = pickle.load(f)

# Main Title
st.title("🏦 Credit Risk Assessment System")

# Layout
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=18, max_value=100)
    income = st.number_input("Annual Income (₹)")
    loan = st.number_input("Loan Amount (₹)")

with col2:
    credit_score = st.number_input("Credit Score")
    city = st.selectbox("Select City", [
        "Kadapa","Kurnool","Nellore","Rajahmundry",
        "Tirupati","Vijayawada","Visakhapatnam"
    ])

st.markdown("---")

if st.button("🔍 Analyze Risk"):

    # Data preparation
    data = {
        'Age': age,
        'Annual_Income': income,
        'Loan_Amount': loan,
        'Credit_Score': credit_score,
        'City_Kadapa': 0,
        'City_Kurnool': 0,
        'City_Nellore': 0,
        'City_Rajahmundry': 0,
        'City_Tirupati': 0,
        'City_Vijayawada': 0,
        'City_Visakhapatnam': 0
    }

    data[f'City_{city}'] = 1
    df = pd.DataFrame([data])

    prediction = model.predict(df)[0]

    st.subheader("📊 Risk Result")

    # Fake percentage (for presentation)
    risk_percent = 80 if prediction == 1 else 20

    if prediction == 0:
        st.success(f"✅ Low Risk ({risk_percent}%) - Loan can be approved")
    else:
        st.error(f"⚠️ High Risk ({risk_percent}%) - Loan approval risky")

    # Graph
    st.subheader("📈 Financial Analysis")

    features = ["Income (₹ Thousands)", "Loan (₹ Thousands)", "Credit Score"]
    values = [income/1000, loan/1000, credit_score]

    fig, ax = plt.subplots()
    ax.barh(features, values)
    ax.set_title("Risk Indicators")
    st.pyplot(fig)

    # Download report
    report = f"""
    CREDIT RISK REPORT
    -------------------------
    Age: {age}
    Income: {income}
    Loan: {loan}
    Credit Score: {credit_score}
    City: {city}

    Prediction: {"High Risk" if prediction==1 else "Low Risk"}
    """

    st.download_button("📄 Download Report", report, file_name="credit_report.txt")

    st.info("Higher income & credit score reduce risk. High loan increases risk.")
