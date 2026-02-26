import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# Load model
with open("Credit_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("Credit Risk Assessment App")

st.write("Enter Customer Details")

# Inputs
age = st.number_input("Age", min_value=18, max_value=100)
income = st.number_input("Annual Income")
loan = st.number_input("Loan Amount")
credit_score = st.number_input("Credit Score")

city = st.selectbox("City", [
    "Kadapa",
    "Kurnool",
    "Nellore",
    "Rajahmundry",
    "Tirupati",
    "Vijayawada",
    "Visakhapatnam"
])

if st.button("Predict"):

    # Create base data
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

    # Activate selected city
    data[f'City_{city}'] = 1

    df = pd.DataFrame([data])

    prediction = model.predict(df)[0]

    if prediction == 0:
        st.success("Customer is Low Risk")
    else:
        st.error("Customer is High Risk")

    # Graph
    features = ["Income (₹ Thousands)",
                "Loan (₹ Thousands)",
                "Credit Score"]

    values = [income/1000,
              loan/1000,
              credit_score]

    fig, ax = plt.subplots()
    ax.barh(features, values)
    ax.set_title("Credit Risk Factors")
    st.pyplot(fig)
