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

# Title
st.title("🏦 Credit Risk Assessment System")

# Input layout
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=18, max_value=100)
    income = st.number_input("Annual Income (₹)")
    loan = st.number_input("Loan Amount (₹)")

with col2:
    credit_score = st.number_input("Credit Score (300–900)")
    city = st.selectbox("Select City", [
        "Kadapa","Kurnool","Nellore","Rajahmundry",
        "Tirupati","Vijayawada","Visakhapatnam"
    ])

st.markdown("---")

if st.button("🔍 Analyze Risk"):

    # Real-world rule-based decision
    if credit_score < 600 or loan > income * 1.5 or income < 200000:
        prediction = 1
    else:
        prediction = 0

    # Display Result
    st.subheader("📊 Final Risk Decision")

    if prediction == 0:
        st.success("✅ Low Credit Risk - Loan can be approved")
    else:
        st.error("⚠️ High Credit Risk - Loan approval risky")

    # Graph
    st.subheader("📈 Financial Analysis")

    features = ["Income (₹ Thousands)", "Loan (₹ Thousands)", "Credit Score"]
    values = [income/1000, loan/1000, credit_score]

    with st.container():
        col1, col2, col3 = st.columns([2,3,2])

        with col2:
            fig, ax = plt.subplots(figsize=(5,3))

            ax.barh(features, values, color="#0a3d62")

            ax.set_title("Risk Indicators", fontsize=10)
            ax.set_xlabel("Scaled Values", fontsize=9)

            ax.set_xlim(0, max(values)*1.25)

            for i, v in enumerate(values):
                ax.text(v + max(values)*0.03, i, f"{round(v,2)}", va='center', fontsize=8)

            st.pyplot(fig)

    # Report
    report = f"""
    CREDIT RISK REPORT
    -------------------------
    Age: {age}
    Income: {income}
    Loan: {loan}
    Credit Score: {credit_score}
    City: {city}

    Final Prediction: {"High Risk" if prediction==1 else "Low Risk"}
    """

    st.download_button("📄 Download Report", report, file_name="credit_report.txt")

    st.info("This system evaluates credit risk based on financial indicators.")
