import streamlit as st
import pandas as pd
import mysql.connector

# --- DB Config ---
db = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user="31CJB1UZRWYNAok.root",
    password="EXpTVqVAmtIV7SY8",
    port=4000,
    database="UG"
)
cursor = db.cursor(dictionary=True)

# --- Query helper ---
def run_query(query):
    cursor.execute(query)
    return pd.DataFrame(cursor.fetchall())

# --- Sidebar filters ---
st.sidebar.title("🎛 Filters")
batch = st.sidebar.text_input("Batch (e.g. Batch-21)")
city = st.sidebar.text_input("City")

# --- Header ---
st.title("🎓 Student Placement Dashboard")

# --- Students ---
student_query = "SELECT * FROM Students"
if batch:
    student_query += f" WHERE course_batch = '{batch}'"
elif city:
    student_query += f" WHERE city = '{city}'"

students_df = run_query(student_query)
st.subheader("👥 Students")
st.dataframe(students_df)

# --- Programming Data ---
st.subheader("💻 Programming Stats")
prog_df = run_query("""
    SELECT s.student_id, s.name, p.language, p.problems_solved, p.latest_project_score
    FROM Students s
    JOIN Programming p ON s.student_id = p.student_id
""")
st.dataframe(prog_df)

# --- Soft Skills ---
st.subheader("🧠 Soft Skills")
skills_df = run_query("""
    SELECT s.student_id, s.name, ss.communication, ss.teamwork, ss.leadership
    FROM Students s
    JOIN SoftSkills ss ON s.student_id = ss.student_id
""")
st.dataframe(skills_df)

# --- Placements ---
st.subheader("🏢 Placement Status")
placement_df = run_query("""
    SELECT s.student_id, s.name, p.placement_status, p.company_name
    FROM Students s
    JOIN Placements p ON s.student_id = p.student_id
""")
st.dataframe(placement_df)

# --- Clean up ---
cursor.close()
db.close()
