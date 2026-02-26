import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# Load model
with open("Credit_model.pkl", "rb") as f:
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
    features = ['Age','Annual_Income','Loan_Amount','Credit_Score']
    values = [age, income, loan, credit_score]

    fig, ax = plt.subplots()
    ax.barh(features, values)
    ax.set_xlabel("Values")
    st.pyplot(fig)
