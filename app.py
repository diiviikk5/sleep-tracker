import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import random
import time

st.set_page_config(page_title="BSDK SOJAYA KAR", layout="wide")


def show_loading_screen():
    random_facts = [
        "Soke dekh bhai ache sapne bhi aate hai",
        "Pura din bhi nahi sona chaiye ",
        "Exam me bina soye jayega to ache se lag jayenge",
        "Kisi din uske saath bhi soyega💖💖",
        "Ek din pehle padhne ke liye Neend mat kharab kar"
    ]
    fact = random.choice(random_facts)
    loading_placeholder = st.empty()
    progress_bar = st.progress(0)
    
    with loading_placeholder.container():
        st.markdown(
            f"""
            <div style="text-align: center; font-size: 30px; font-weight: bold; margin-top: 20vh;">
                ⏳ Loading...
            </div>
            <div style="text-align: center; font-size: 24px; margin-top: 10px;">
                {fact}
            </div>
            """, unsafe_allow_html=True
        )
    
    for i in range(1, 101, 10):
        time.sleep(0.2)
        progress_bar.progress(i)
    
    time.sleep(2)
    loading_placeholder.empty()
    progress_bar.empty()

show_loading_screen()

st.title("BSDK SOJAYA KAR")

st.sidebar.header("Enter Your Sleep Data")
sleep_hours = []

for i in range(7):
    day = (datetime.today() - timedelta(days=i)).strftime("%A")
    sleep = st.sidebar.number_input(f"Hours Slept on {day}", min_value=0.0, max_value=12.0, step=0.5, key=f"day_{i}")
    sleep_hours.append(sleep)


df = pd.DataFrame({"Day": [(datetime.today() - timedelta(days=i)).strftime("%A") for i in range(7)], "Sleep Hours": sleep_hours})
recommended_hours = 8  
df["Sleep Deficit"] = recommended_hours - df["Sleep Hours"]

st.subheader("📅 Your Weekly Sleep Pattern")
st.dataframe(df)

fig = px.line(df, x="Day", y="Sleep Hours", title="Your Sleep Trend (Last 7 Days)", markers=True)
st.plotly_chart(fig)


total_deficit = df["Sleep Deficit"].sum()
st.subheader(f" Total Sleep Debt: {total_deficit:.1f} hours")


reaction_time_increase = total_deficit * 5  
productivity_drop = min(total_deficit * 3, 100)  

st.subheader(" Estimated Impact on Cognitive Performance")
st.write(f" **Reaction Time Delay:** +{reaction_time_increase:.1f}%")
st.write(f" **Productivity Drop:** {productivity_drop:.1f}%")


if sum(sleep_hours) > 0:
    X = np.array([[i] for i in range(1, 11)]) 
    y = np.array([90, 85, 75, 60, 50, 40, 30, 20, 10, 5])  

    model = LinearRegression()
    model.fit(X, y)
    predicted_fatigue = model.predict(np.array([[sum(sleep_hours) / 7]]))[0]

    st.subheader(" Predicted Fatigue Risk")
    st.progress(int(predicted_fatigue))
    st.write(f" **Your Fatigue Risk Level:** {predicted_fatigue:.1f}%")
else:
    st.subheader(" Predicted Fatigue Risk")
    st.write(" Enter sleep data to calculate fatigue risk.")

if total_deficit > 0:
    st.subheader("🌙 Recommended Sleep Recovery Plan")
    recovery_hours = total_deficit / 3  
    st.write(f"Try sleeping **{recommended_hours + recovery_hours:.1f} hours** per night for the next 3 days to recover.")


challenges = [
    "Do 10 minutes of stretching before bed",
    "Try 5 minutes of deep breathing meditation",
    "No screen usage 30 minutes before bedtime",
    "Read a book for 15 minutes",
    "Write down 3 things you're grateful for",
    "Take a warm shower before bed",
    "Listen to relaxing music for 10 minutes",
    "Avoid caffeine in the evening"
]

def spin_wheel():
    st.subheader("🎡 Spinning the Wheel...")
    progress_bar = st.progress(0)
    for i in range(1, 101, 10):
        time.sleep(0.1)
        progress_bar.progress(i)
    progress_bar.empty()
    return random.choice(challenges)

if total_deficit > 0:
    st.subheader("🎡 Sleep Debt TASKS")
    st.warning("You're in sleep debt! Spin the wheel for a TASK.")
    st.write(" TASKS:")
    for challenge in challenges:
        st.write(f"- {challenge}")
    
    if st.button("🎡 Spin the Wheel!"):
        challenge = spin_wheel()
        st.success(f"Your Challenge: {challenge}")

st.success("🔄 Keep tracking your sleep to optimize your health and performance!")
