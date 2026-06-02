import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("model/model.pkl", "rb"))

# Title
st.title("AI Placement Prediction Dashboard")

# Inputs
cgpa = st.slider("Enter CGPA", 0.0, 10.0, 7.0)

aptitude = st.slider("Enter Aptitude Score", 0, 100, 60)

internship = st.selectbox(
    "Internship Completed?",
    [0, 1]
)

# Prediction
if st.button("Predict Placement"):

    prediction = model.predict(

        [[cgpa, aptitude, internship]]
    )

    if prediction[0] == 1:
        st.success("High Chance of Placement")
    else:
        st.error("Low Chance of Placement")

 import matplotlib.pyplot as plt

chart_data = [cgpa, aptitude]

fig, ax = plt.subplots()

ax.bar(
    ['CGPA', 'Aptitude'],
    chart_data
)

st.pyplot(fig)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)