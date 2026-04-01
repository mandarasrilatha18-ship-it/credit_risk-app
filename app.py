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

    # Prepare ML input
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

    # ML Prediction
    ml_prediction = model.predict(df)[0]

    # Real-world rule-based prediction
    reasons = []

    if credit_score < 600:
        reasons.append("Low credit score")

    if loan > income * 1.5:
        reasons.append("Loan is very high compared to income")

    if income < 200000:
        reasons.append("Low income")

    if len(reasons) > 0:
        real_prediction = 1
    else:
        real_prediction = 0

    # Display Results
    st.subheader("📊 Risk Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🤖 ML Prediction")
        if ml_prediction == 0:
            st.success("Low Risk")
        else:
            st.error("High Risk")

    with col2:
        st.markdown("### 🏦 Real-World Prediction")
        if real_prediction == 0:
            st.success("Low Risk (Realistic)")
        else:
            st.error("High Risk (Realistic)")

    # Reasons
    if real_prediction == 1:
        st.warning("⚠️ Reasons:")
        for r in reasons:
            st.write(f"- {r}")

    # GRAPH (FINAL FIXED SIZE)
    st.subheader("📈 Financial Analysis")

    features = ["Income (₹ Thousands)", "Loan (₹ Thousands)", "Credit Score"]
    values = [income/1000, loan/1000, credit_score]

    with st.container():
        col1, col2, col3 = st.columns([2,3,2])

        with col2:
            fig, ax = plt.subplots(figsize=(5,3))  # 👈 FIXED SIZE

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

    ML Prediction: {"High Risk" if ml_prediction==1 else "Low Risk"}
    Real Prediction: {"High Risk" if real_prediction==1 else "Low Risk"}

    Reasons: {', '.join(reasons) if reasons else "No major risk"}
    """

    st.download_button("📄 Download Report", report, file_name="credit_report.txt")

    st.info("Real-world prediction considers credit score, income stability, and loan burden.")
