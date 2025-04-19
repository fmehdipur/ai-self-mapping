import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from fpdf import FPDF
import sqlite3

st.set_page_config(page_title="AI-Augmented Self-Mapping", layout="centered")

# Add custom logo and tagline
st.image("logo.jpg", width=150)
st.markdown("<h1 style='font-size: 24px;'>AI for Life.<br>One Byte at a Time.</h1>", unsafe_allow_html=True)

# --- Landing Page Content ---
st.markdown("""
## 🧠 AI-Augmented Self-Mapping
Helping you reflect, adapt, and lead — one byte at a time.

### 🔍 What It Is
AI-Augmented Self-Mapping (AI-SM) is a personal insight tool that helps individuals and teams understand:
- How they think
- How they decide
- How they grow over time

This tool uses intelligent prompts and analytics to support reflection and improvement in leadership, learning, and collaboration.

### 🎯 Who It's For
- Educators & academic leaders
- Postgraduate students
- Startups & innovation teams
- Coaches and consultants

### 🧾 Key Features
- Real-time insight generation
- Capability charts with PDF summaries
- Session tagging and trend tracking
- Private and ethical data use

### 🚀 Try It Now
Use the form below to begin your personalised reflection and self-mapping journey.

---
""")

# --- SQLite setup ---
conn = sqlite3.connect("user_sessions.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag TEXT,
    reflection TEXT,
    pace INTEGER,
    emotion TEXT,
    decision TEXT,
    confidence INTEGER,
    collaboration TEXT
)''')
conn.commit()

# --- UI input ---
st.markdown("### 🧠 Weekly Self-Mapping Reflection")

with st.form("reflection_form"):
    tag = st.text_input("Enter a session tag or name (e.g., Week 3, Sprint A, Self Check)")
    reflection = st.text_area("What recent situation challenged your thinking or decision-making?")
    pace = st.slider("How would you rate your work pace this week?", 1, 10, 5)
    emotion = st.radio("What best describes your emotional response to challenges?", ["Calm and analytical", "Reactive but adaptive", "Overwhelmed", "Confident and assertive"])
    decision = st.radio("How do you typically make decisions under pressure?", ["Quick and instinctive", "Calculated and cautious", "Delegated", "Avoided or delayed"])
    confidence = st.slider("Rate your self-confidence this week", 1, 10, 6)
    collaboration = st.radio("How did you engage in team collaboration recently?", ["Led decisively", "Listened actively", "Avoided conflict", "Remained passive"])
    submitted = st.form_submit_button("Generate Insights")

if submitted:
    c.execute('''INSERT INTO sessions (tag, reflection, pace, emotion, decision, confidence, collaboration)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (tag, reflection, pace, emotion, decision, confidence, collaboration))
    conn.commit()

    session_id = c.lastrowid
    st.markdown("---")
    st.markdown(f"### 🧾 Personalised Insight Profile (Session {session_id})")

    # Compute scores
    scores = {
        "Pace": pace,
        "Emotion": 10 if emotion == "Calm and analytical" else 7 if emotion == "Reactive but adaptive" else 4 if emotion == "Overwhelmed" else 9,
        "Decision": 6 if decision == "Quick and instinctive" else 8 if decision == "Calculated and cautious" else 7 if decision == "Delegated" else 4,
        "Confidence": confidence,
        "Collaboration": 9 if collaboration == "Led decisively" else 8 if collaboration == "Listened actively" else 5 if collaboration == "Avoided conflict" else 3
    }

    # Chart for Streamlit
    chart_data = pd.DataFrame({"Trait": list(scores.keys()), "Score": list(scores.values())})
    fig, ax = plt.subplots()
    ax.bar(chart_data["Trait"], chart_data["Score"], color='#0A66C2')
    ax.set_ylim([0, 10])
    ax.set_ylabel("Score")
    ax.set_title(f"{tag or 'Session ' + str(session_id)} Capability Map")
    st.pyplot(fig)

    # Save chart image for PDF
    chart_path = "capability_chart.png"
    fig.savefig(chart_path)
    plt.close()

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "AI-Augmented Self-Mapping Summary", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Reflection Summary:\n{reflection}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Pace: {pace} - High cognitive pace, effective under pressure.")
    pdf.multi_cell(0, 10, f"Emotion: {emotion} - {('Confident and assertive leadership.' if emotion == 'Confident and assertive' else 'Emotionally responsive.')}")
    pdf.multi_cell(0, 10, f"Decision Style: {decision} - Adaptive and strategic.")
    pdf.multi_cell(0, 10, f"Confidence: {confidence} - Consistent and assertive.")
    pdf.multi_cell(0, 10, f"Collaboration: {collaboration} - Proactive engagement with your team.")
    pdf.ln(10)
    pdf.image(chart_path, x=25, w=160)

    pdf_path = "AI_SelfMapping_Summary_Report.pdf"
    pdf.output(pdf_path)

    with open(pdf_path, "rb") as f:
        st.download_button("Download Summary Report as PDF", f, file_name="AI_SelfMapping_Summary_Report.pdf")

# Show previous sessions with analytics
c.execute("SELECT * FROM sessions")
rows = c.fetchall()
if rows:
    df = pd.DataFrame(rows, columns=["ID", "Tag", "Reflection", "Pace", "Emotion", "Decision", "Confidence", "Collaboration"])
    st.markdown("### 📊 Enhanced Analytics and Trends")
    st.line_chart(df.set_index("ID")[['Pace', 'Confidence']])
    st.bar_chart(df["Emotion"].value_counts())
    st.bar_chart(df["Collaboration"].value_counts())
    st.caption("Tracking multiple dimensions of growth and behaviour across sessions.")

st.divider()

st.markdown("""
### 🔧 Core Features
- Reflection-based input and behavioural analysis
- Generative AI engine for personalised insight
- Visual self-mapping dashboard and progress tracker
- Session tagging and history with analytics
- Ethics-first design with full user control

### 🎯 Use Cases
- Academic leadership development
- Postgraduate student growth planning
- Startup team alignment and decision profiling

### 🤝 Let’s Collaborate
We’re seeking partners for research, co-development, and pilot implementation.

📩 hello@yourdomain.com  
🔗 [Connect on LinkedIn](https://www.linkedin.com/in/farhad-mehdipour-111245b/)
""")

st.success("Prototype version — with landing content, session tags, analytics, and insight export")
