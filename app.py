import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import random
import time
import os
import streamlit.components.v1 as components


st.set_page_config(page_title="🧠 SOJA BHAI", layout="wide", initial_sidebar_state="expanded")

# Load HTML and CSS with full JS support
def load_assets():
    try:
        # HTML content embedded with Typewriter effect and Clock functionality
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap" rel="stylesheet">
            <style>
                body {
                    background-color: #121212;
                    color: white;
                    font-family: 'Orbitron', sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                    overflow: hidden;
                }
                .orbitron-banner {
                    text-align: center;
                    margin-bottom: 20px;
                }
                .orbitron-title {
                    font-size: 3em;
                    margin-bottom: 10px;
                }
                .orbitron-subtitle {
                    font-size: 1.5em;
                    color: cyan;
                }
                #clock {
                    font-size: 1.2em;
                    margin-bottom: 15px;
                }
                #greet-msg {
                    margin-top: 15px;
                    font-size: 1.2em;
                    color: lightgreen;
                    opacity: 0;
                    transition: opacity 0.5s ease;
                }
                /* Loader Styles */
                #loader {
                    border: 5px solid #1DB954;
                    border-top: 5px solid cyan;
                    border-radius: 50%;
                    width: 50px;
                    height: 50px;
                    animation: spin 1s linear infinite;
                    margin-bottom: 20px;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                /* Hide loader after content is ready */
                #loader.hidden {
                    display: none;
                }
            </style>
        </head>
        <body>

        <!-- Loader -->
        <div id="loader"></div>

        <div class="orbitron-banner" id="content" style="display: none;">
            <h1 class="orbitron-title">SOJA BHAI 🧠</h1>
            <p class="orbitron-subtitle" id="typewriter"></p>
        </div>

        <div id="clock"></div>

        <p id="greet-msg"></p>

        <script>
            // Show loader until the content is ready
            window.onload = () => {
                document.getElementById("loader").classList.add("hidden");
                document.getElementById("content").style.display = "block";
                setTimeout(showGreeting, 3000); // Show greeting after 3 seconds
            };

            // Typewriter Effect
            const text = "Sleep Tracker • Fatigue Monitor • Performance Booster";
            let index = 0;
            const speed = 75;

            function typeWriter() {
                if (index < text.length) {
                    document.getElementById("typewriter").innerHTML += text.charAt(index);
                    index++;
                    setTimeout(typeWriter, speed);
                }
            }
            typeWriter();

            // Real-Time Clock
            function updateTime() {
                const now = new Date();
                const timeString = now.toLocaleTimeString();
                document.getElementById('clock').innerText = "Current Time: " + timeString;
            }
            setInterval(updateTime, 1000);

            // Show greeting after the typewriter effect finishes
            function showGreeting() {
                const msg = document.getElementById('greet-msg');
                msg.innerText = "Arrey Ab so bhi ja mere bhai ! 🛌";
                msg.style.opacity = 1; // Smooth fade-in
            }
        </script>

        </body>
        </html>
        """
        # Render the full HTML with JS
        components.html(html_content, height=600)
    except Exception as e:
        st.error(f"Error loading HTML: {e}")


if 'loaded' not in st.session_state:
    def show_loading_screen():
        random_facts = [
            "😴 Soke dekh bhai ache sapne bhi aate hai",
            "🚫 Pura din bhi nahi sona chaiye",
            "📚 Exam me bina soye jayega to ache se lag jayenge",
            "🛌 Neend ki kami se productivity kam hoti hai",
            "📖 Ek din pehle padhne ke liye Neend mat kharab kar"
        ]
        fact = random.choice(random_facts)
        loading_placeholder = st.empty()
        progress_bar = st.progress(0)

        with loading_placeholder.container():
            st.image("image.png", width=150)    
            st.markdown(
                f"""
                <div style="text-align: center; font-size: 36px; font-weight: bold; margin-top: 2vh; color: cyan;">
                    ⚙️ Booting SOJA BHAI...
                </div>
                <div style="text-align: center; font-size: 20px; color: #bbb;">
                    {fact}
                </div>
                """, unsafe_allow_html=True
            )

        for i in range(1, 101, 10):
            time.sleep(0.1)
            progress_bar.progress(i)

        time.sleep(1)
        loading_placeholder.empty()
        progress_bar.empty()

    show_loading_screen()
    st.session_state.loaded = True


load_assets()


st.markdown('<h2 style="color: violet;">Welcome to SOJA BHAI</h2>', unsafe_allow_html=True)
st.markdown("Track. Analyze. Optimize.", unsafe_allow_html=True)
st.image("2.png", use_container_width=True)
st.image("3.png", use_container_width=True)


st.sidebar.title("🛌 Enter Your Sleep Data")
sleep_hours = []
for i in range(7):
    day = (datetime.today() - timedelta(days=i)).strftime("%A")
    sleep = st.sidebar.slider(f"Hours Slept on {day}", min_value=0.0, max_value=12.0, step=0.5, key=f"day_{i}")
    sleep_hours.append(sleep)


df = pd.DataFrame({
    "Day": [(datetime.today() - timedelta(days=i)).strftime("%A") for i in range(7)],
    "Sleep Hours": sleep_hours
})

recommended_hours = 8
df["Sleep Deficit"] = recommended_hours - df["Sleep Hours"]
total_deficit = df["Sleep Deficit"].sum()
total_sleep = sum(sleep_hours)


fatigue_risk = 0
if total_sleep > 0:
    model = LinearRegression()
    X = np.array([[i] for i in range(1, 11)])
    y = np.array([90, 85, 75, 60, 50, 40, 30, 20, 10, 5])
    model.fit(X, y)
    fatigue_risk = model.predict(np.array([[total_sleep / 7]]))[0]


with st.container():
    st.markdown("## 🔍 Weekly Sleep Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("💤 Total Sleep", f"{total_sleep:.1f} hrs")
    col2.metric("⚠️ Sleep Debt", f"{total_deficit:.1f} hrs")
    col3.metric("🧠 Fatigue Risk", f"{fatigue_risk:.1f}%")
    st.plotly_chart(px.line(df, x="Day", y="Sleep Hours", title="🌙 Sleep Pattern (Last 7 Days)", markers=True))
    st.dataframe(df, use_container_width=True)


reaction_time_increase = total_deficit * 5
productivity_drop = min(total_deficit * 3, 100)

st.markdown("## 🧠 Performance Impact")
col4, col5 = st.columns(2)
col4.success(f"⏳ Reaction Time Delay: +{reaction_time_increase:.1f}%")
col5.error(f"📉 Productivity Drop: {productivity_drop:.1f}%")
st.image("4.png", width=400)

if total_deficit > 0:
    st.markdown("## 🌌 Recovery Plan")
    recovery_hours = total_deficit / 3
    st.info(f"For the next 3 nights, try sleeping **{recommended_hours + recovery_hours:.1f} hours** each night.")

challenges = [
    "Do 10 minutes of stretching before bed",
    "Try 5 minutes of deep breathing meditation",
    "No screen usage 30 minutes before bedtime",
    "Read a book for 15 minutes",
    "Take a warm shower before bed",
    "Listen to relaxing music for 10 minutes",
    "Avoid caffeine in the evening"
]

def spin_wheel():
    st.toast("🎡 Spinning the wheel...")
    bar = st.progress(0)
    for i in range(1, 101, 10):
        time.sleep(0.05)
        bar.progress(i)
    bar.empty()
    return random.choice(challenges)

if total_deficit > 0:
    st.markdown("## 🎯 Sleep Improvement Challenge")
    st.warning("You're in sleep debt. Complete a challenge to rebuild your sleep habits!")
    if st.button("🎡 Spin the Challenge Wheel"):
        challenge = spin_wheel()
        st.write(f"✅ Challenge: {challenge}")
