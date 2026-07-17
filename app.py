import streamlit as st
import random
import time
import pandas as pd
import os

# File for leaderboard
LEADERBOARD_FILE = "leaderboard.csv"

# Ensure leaderboard exists
if not os.path.exists(LEADERBOARD_FILE):
    pd.DataFrame(columns=["Name", "Score"]).to_csv(LEADERBOARD_FILE, index=False)

st.set_page_config(page_title="🧠 Memory Card Challenge", layout="centered")

# Initialize session state
if "game_state" not in st.session_state:
    st.session_state.game_state = "login"
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.sequence = []
    st.session_state.player_name = ""

def save_score(name, score):
    df = pd.read_csv(LEADERBOARD_FILE)
    new_entry = pd.DataFrame([[name, score]], columns=["Name", "Score"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(LEADERBOARD_FILE, index=False)

st.title("🧠 Memory Card Challenge")

if st.session_state.game_state == "login":
    st.session_state.player_name = st.text_input("Enter your name to start:")
    if st.button("Start Game"):
        if st.session_state.player_name:
            st.session_state.game_state = "start"
            st.rerun()

elif st.session_state.game_state == "start":
    difficulty = st.radio("Choose Difficulty", ["Easy", "Medium", "Hard"])
    if st.button("Start Round"):
        items = ["Apple", "Car", "Moon", "Star", "Book", "Pen", "Tree", "Bird", "Sun", "Desk", "Lamp"]
        count = {"Easy": 5, "Medium": 10, "Hard": 15}[difficulty]
        st.session_state.sequence = random.sample(items, count)
        st.session_state.game_state = "memory"
        st.rerun()

elif st.session_state.game_state == "memory":
    st.subheader("Remember this sequence!")
    st.write(st.session_state.sequence)
    placeholder = st.empty()
    for i in range(5, 0, -1):
        placeholder.write(f"Time remaining: {i} seconds")
        time.sleep(1)
    st.session_state.game_state = "recall"
    st.rerun()

elif st.session_state.game_state == "recall":
    st.subheader("Type what you remember (separated by spaces)")
    user_input = st.text_input("Your Answer")
    if st.button("Submit"):
        # Normalization: Case-insensitive comparison 
        user_list = user_input.lower().split()
        sequence_list = [item.lower() for item in st.session_state.sequence]
        
        st.session_state.total += 1
        if user_list == sequence_list:
            st.session_state.score += 1
            st.success("🎉 Congratulations! That's correct!")
        else:
            st.error(f"❌ Try next time! The correct sequence was: {st.session_state.sequence}")
        
        time.sleep(2)
        st.session_state.game_state = "result"
        st.rerun()

elif st.session_state.game_state == "result":
    st.write(f"Current Session Score: {st.session_state.score} / {st.session_state.total}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Next Round"):
            st.session_state.game_state = "start"
            st.rerun()
    with col2:
        if st.button("End Game & Save Score"):
            save_score(st.session_state.player_name, st.session_state.score)
            st.balloons()
            st.session_state.game_state = "leaderboard"
            st.rerun()

elif st.session_state.game_state == "leaderboard":
    st.subheader("🏆 Leaderboard")
    df = pd.read_csv(LEADERBOARD_FILE)
    st.table(df.sort_values(by="Score", ascending=False))
    if st.button("Back to Main Menu"):
        st.session_state.game_state = "login"
        st.session_state.score = 0
        st.session_state.total = 0
        st.rerun()