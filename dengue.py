import streamlit as st
import pickle
import numpy as np

# Load the trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

st.set_page_config(page_title="Disease Prediction", page_icon="🩺", layout="centered")

st.title("🩺 Disease Prediction App")
st.write("Enter the patient details below to predict the result.")

# Input fields
Gender = st.selectbox("Gender", ["Male", "Female"])
Age = st.number_input("Age", min_value=0, max_value=120, step=1)
Haemoglobin = st.number_input("Haemoglobin", min_value=0.0, step=0.1)
ESR = st.number_input("ESR", min_value=0.0, step=0.1)
WBC = st.number_input("WBC", min_value=0.0, step=0.1)
Neutrophil = st.number_input("Neutrophil", min_value=0, max_value=100, step=1)
Lymphocyte = st.number_input("Lymphocyte", min_value=0.0, step=0.1)
Monocyte = st.number_input("Monocyte", min_value=0.0, step=0.1)
Eosinophil = st.number_input("Eosinophil", min_value=0.0, step=0.1)
Basophil = st.number_input("Basophil", min_value=0.0, step=0.1)
RBC = st.number_input("RBC", min_value=0.0, step=0.1)
Platelets = st.number_input("Platelets", min_value=0, step=1)

# Convert gender to numeric
Gender_val = 1 if Gender == "Male" else 0

# Prediction button
if st.button("Predict"):
    input_data = np.array([[Gender_val, Age, Haemoglobin, ESR, WBC,
                            Neutrophil, Lymphocyte, Monocyte, Eosinophil,
                            Basophil, RBC, Platelets]])
    pred = model.predict(input_data)[0]
    result = "✅ Positive" if pred == 1 else "❌ Negative"
    st.subheader(f"Prediction Result: {result}")
