import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np

# Load model
with open("Credit_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("Credit Risk Assessment App")

st.write("Enter customer details below:")

age = st.number_input("Age", min_value=18, max_value=100)
income = st.number_input("Annual Income")
loan = st.number_input("Loan Amount")
credit_score = st.number_input("Credit Score")

if st.button("Predict"):

    # Create input as numpy array (avoids feature name issues)
    data = np.array([[age, income, loan, credit_score]])

    prediction = model.predict(data)[0]

    if prediction == 0:
        st.success("Customer is Low Risk")
    else:
        st.error("Customer is High Risk")

    # Graph (scaled for clarity)
    features = ['Income (₹ Thousands)', 
                'Loan (₹ Thousands)', 
                'Credit Score']

    values = [income/1000, 
              loan/1000, 
              credit_score]

    fig, ax = plt.subplots()
    ax.barh(features, values)
    ax.set_xlabel("Scaled Values")
    ax.set_title("Credit Risk Assessment Factors")
    st.pyplot(fig)

    st.info("Higher credit score generally indicates lower credit risk.")
