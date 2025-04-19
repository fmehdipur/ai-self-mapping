import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import json

st.set_page_config(page_title="AI-Augmented Self-Mapping", layout="centered")

st.title("AI-Augmented Self-Mapping")
st.subheader("Redefining Capability Insight for the Human-AI Era")

# Load session data if exists
DATA_FILE = "user_sessions.json"
sessions = []
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        sessions = json.load(f)

st.markdown("### 🧠 Weekly Self-Mapping Reflection")

with st.form("reflection_form"):
    reflection = st.text_area("What recent situation challenged your thinking or decision-making?")
    pace = st.slider("How would you rate your work pace this week?", 1, 10, 5)
    emotion = st.radio("What best describes your emotional response to challenges?", ["Calm and analytical", "Reactive but adaptive", "Overwhelmed", "Confident and assertive"])
    decision = st.radio("How do you typically make decisions under pressure?", ["Quick and instinctive", "Calculated and cautious", "Delegated", "Avoided or delayed"])
    confidence = st.slider("Rate your self-confidence this week", 1, 10, 6)
    collaboration = st.radio("How did you engage in team collaboration recently?", ["Led decisively", "Listened actively", "Avoided conflict", "Remained passive"])
    submitted = st.form_submit_button("Generate Insights")

if submitted:
    current = {
        "Reflection": reflection,
        "Pace": pace,
        "Emotion": emotion,
        "Decision": decision,
        "Confidence": confidence,
        "Collaboration": collaboration
    }
    sessions.append(current)
    with open(DATA_FILE, "w") as f:
        json.dump(sessions, f)

    st.markdown("---")
    st.markdown("### 🧾 Personalised Insight Profile (Session {})".format(len(sessions)))

    # Display insights based on current input
    def display_insights(pace, emotion, decision, confidence, collaboration):
        if pace >= 8:
            st.success("🧠 High cognitive pace: Strong urgency. Schedule reflection time.")
        elif pace >= 5:
            st.info("🧠 Balanced pace: Maintain your rhythm and priorities.")
        else:
            st.warning("🧠 Slower pace: Clarify goals and energy levels.")

        if emotion == "Calm and analytical":
            st.success("💬 Regulated emotion: Ideal for leadership.")
        elif emotion == "Reactive but adaptive":
            st.info("💬 Adaptive: Consider pausing before action.")
        elif emotion == "Overwhelmed":
            st.warning("💬 Pressure detected. Evaluate support needs.")
        else:
            st.success("💬 Confident and assertive: Leverage wisely.")

        if decision == "Quick and instinctive":
            st.warning("🧭 Instinctive: Validate rapid decisions.")
        elif decision == "Calculated and cautious":
            st.info("🧭 Cautious: Guard against overanalysis.")
        elif decision == "Delegated":
            st.info("🧭 Delegated: Balance ownership with input.")
        else:
            st.warning("🧭 Avoidance: Understand the root causes.")

        if confidence >= 8:
            st.success("🚀 Strong confidence: Channel it with balance.")
        elif confidence >= 5:
            st.info("🚀 Grounded confidence: Build on consistent progress.")
        else:
            st.warning("🚀 Low confidence: Reflect on achievements and regain clarity.")

        if collaboration == "Led decisively":
            st.success("🤝 You are leading actively.")
        elif collaboration == "Listened actively":
            st.info("🤝 Empathic collaborator.")
        elif collaboration == "Avoided conflict":
            st.warning("🤝 Conflict avoidance. Surface tensions constructively.")
        else:
            st.warning("🤝 Passive engagement. Reconnect with your role.")

    display_insights(pace, emotion, decision, confidence, collaboration)

    # Display radar chart for current session
    chart_data = pd.DataFrame({
        "Trait": ['Pace', 'Emotion', 'Decision', 'Confidence', 'Collaboration'],
        "Score": [pace, 10 if emotion == "Calm and analytical" else 7 if emotion == "Reactive but adaptive" else 4 if emotion == "Overwhelmed" else 9,
                   6 if decision == "Quick and instinctive" else 8 if decision == "Calculated and cautious" else 7 if decision == "Delegated" else 4,
                   confidence,
                   9 if collaboration == "Led decisively" else 8 if collaboration == "Listened actively" else 5 if collaboration == "Avoided conflict" else 3]
    })
    fig, ax = plt.subplots()
    ax.bar(chart_data["Trait"], chart_data["Score"], color='cornflowerblue')
    ax.set_ylim([0, 10])
    ax.set_ylabel("Score")
    ax.set_title("Session {} Capability Map".format(len(sessions)))
    st.pyplot(fig)

# Show all previous sessions
if sessions:
    st.markdown("### 📈 Progress Over Time")
    session_df = pd.DataFrame(sessions)
    st.line_chart(session_df[['Pace', 'Confidence']])
    st.caption("Tracking your pace and confidence over multiple sessions.")

st.divider()

st.markdown("""
### 🔧 Core Features
- Reflection-based input and behavioural analysis
- Generative AI engine for personalised insight
- Visual self-mapping dashboard and progress tracker
- Ethics-first design with full user control

### 🎯 Use Cases
- Academic leadership development
- Postgraduate student growth planning
- Startup team alignment and decision profiling

### 🤝 Call to Action
We're seeking partners for research, co-development, and pilot implementation.

📩 If you're interested in collaborating, get in touch!
""")

st.success("Prototype version — Streamlit format with session tracking and extended insights")
