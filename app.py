import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# Load trained model
with open("Credit_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("Credit Risk Prediction App")

st.subheader("Enter Customer Details")

# User Inputs
age = st.number_input("Age", min_value=18, max_value=100)
income = st.number_input("Annual Income")
loan = st.number_input("Loan Amount")
credit_score = st.number_input("Credit Score")

city = st.selectbox("Select City", [
    "Kadapa",
    "Kurnool",
    "Nellore",
    "Rajahmundry",
    "Tirupati",
    "Vijayawada",
    "Visakhapatnam"
])

if st.button("Predict"):

    # Create all city columns with 0
    city_columns = {
        'City_Kadapa': 0,
        'City_Kurnool': 0,
        'City_Nellore': 0,
        'City_Rajahmundry': 0,
        'City_Tirupati': 0,
        'City_Vijayawada': 0,
        'City_Visakhapatnam': 0
    }

    # Set selected city = 1
    city_columns[f'City_{city}'] = 1

    # Create dataframe with ALL required columns
    data = pd.DataFrame([{
        'Age': age,
        'Annual_Income': income,
        'Loan_Amount': loan,
        'Credit_Score': credit_score,
        **city_columns
    }])

    # Prediction
    prediction = model.predict(data)[0]

    if prediction == 0:
        st.success("Customer is Low Risk ✅")
    else:
        st.error("Customer is High Risk ⚠️")

    # Show entered values graph
    features = ['Age','Annual_Income','Loan_Amount','Credit_Score']
    values = [age, income, loan, credit_score]

    fig, ax = plt.subplots()
    ax.barh(features, values)
    ax.set_xlabel("Values")
    st.pyplot(fig)
