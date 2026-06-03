import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import PyPDF2

# Load model
model = pickle.load(open("Model/model.pkl", "rb"))

menu = st.sidebar.selectbox(
    "Select Module",
    ["Student Module", "Admin Module"]
)
#Student Module

if menu == "Student Module":

    st.title("AI Placement Prediction Dashboard")

    student_name = st.text_input("Enter Student Name")

    cgpa = st.slider("Enter CGPA", 0.0, 10.0, 7.0)

    aptitude = st.slider("Enter Aptitude Score", 0, 100, 60)

    internship = st.selectbox("Internship Completed?",["0","1","2","3","4","5","6"])

    internship_value = int(internship)

    if st.button("Predict"):
        st.write("Internship value used:", internship_value)
   
    prediction = None
    if st.button("Predict Placement"):
        prediction = model.predict([[internship_value]])

    if prediction[0] == 1:
        st.success("🎉 Student is Likely Placed")
    else:
        st.error("❌ Student may not be placed")
    #Career  Recommendation
    if cgpa < 7:
        st.warning("Recommendation: Improve your CGPA.")

    if aptitude < 70:
        st.warning("Recommendation: Practice aptitude and reasoning.")

    if internship == 0:
        st.warning("Recommendation: Complete at least one internship.")

    #Charts
    chart_data = [cgpa, aptitude]

    fig, ax = plt.subplots()

    ax.bar(['CGPA', 'Aptitude'],chart_data)

    st.pyplot(fig)

    #Resume Upload
    uploaded_file = st.file_uploader("Upload Resume",type=["pdf"])

    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""

        for page in pdf_reader.pages:
           text += page.extract_text()
    
    #Skill Detection 
        skills = [
            "python",
            "java",
            "sql",
            "power bi",
            "machine learning",
            "excel"
        ]

        found_skills = []
        for skill in skills:
            if skill.lower() in text.lower():
                found_skills.append(skill)

        st.subheader("Detected Skills")
        st.write(found_skills)

        score = 0
        if "python" in found_skills:
            score += 20

        if "sql" in found_skills:
            score += 20

        if "excel" in found_skills:
            score += 15

        if "power bi" in found_skills:
            score += 15

        if "java" in found_skills:
            score += 15

        if "machine learning" in found_skills:
         score += 15

        st.subheader("Resume Score")
        st.success(f"{score}/100")
        st.progress(score/100)

    #Skill Gap Analysis
        required_skills = [
            "python",
            "sql",
            "excel",
            "power bi"
        ]
        missing_skills = []

        for skill in required_skills:
            if skill not in found_skills:
             missing_skills.append(skill)

        st.subheader("Skills To Learn")

        if missing_skills:
            st.write(missing_skills)
        else:
            st.success("All required skills detected!")

#Admin Module 
elif menu == "Admin Module":

    st.title("Admin Dashboard")

    try:
        data =pd.read_csv("students.csv")

        st.subheader("Student Records")
        st.dataframe(data)

        st.subheader("CGPA Analysis")
        st.bar_chart(data["CGPA"])

        st.subheader("Aptitude Analysis")
        st.bar_chart(data["Aptitude"])

        st.metric(
            "Average CGPA",
            round(data["CGPA"].mean(), 2)
        )

        st.metric(
            "Average Aptitude",
            round(data["Aptitude"].mean(), 2)
        )

    except Exception as e:
        st.error(f"Error loading students.csv: {e}")
