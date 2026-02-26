import streamlit as st
import pandas as pd
import pickle
import zipfile
import matplotlib.pyplot as plt

# Unzip model
with open("Credit_model.zip.pkl","rb") as f:
    model = pickle.load(f)

# Load model
with open("Credit_model.pkl","rb") as f:
    model = pickle.load(f)

st.title("Credit Risk Prediction App")

age = st.number_input("Age", min_value=18, max_value=100)
income = st.number_input("Annual Income")
loan = st.number_input("Loan Amount")
credit_score = st.number_input("Credit Score")

if st.button("Predict"):
    data = pd.DataFrame([[age, income, loan, credit_score]],
                        columns=['Age','Annual_Income','Loan_Amount','Credit_Score'])

    prediction = model.predict(data)[0]

    if prediction == 0:
        st.success("Customer is Low Risk")
    else:
        st.error("Customer is High Risk")

    # Simple graph
    features = ['Age','Income','Loan','Credit Score']
    values = [age, income, loan, credit_score]

    plt.barh(features, values)
    plt.xlabel("Values")
    st.pyplot(plt)
