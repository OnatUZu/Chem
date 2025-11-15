import streamlit as st
import pandas as pd
import random
from difflib import SequenceMatcher

data = pd.read_csv("Chem.csv")

name_col = "Element_Name"
symbol_col = "Symbol"

def is_close(answer, correct, threshold=0.8):
    ratio = SequenceMatcher(None, answer.lower().strip(), correct.lower().strip()).ratio()
    return ratio >= threshold

if "questions" not in st.session_state:
    st.session_state.questions = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "results" not in st.session_state:
    st.session_state.results = []
if "started" not in st.session_state:
    st.session_state.started = False

st.title("Chemistry Quiz")
st.write("Test your knowledge of chemical elements and symbols.")

if not st.session_state.started:
    num = st.number_input("How many questions would you like?", min_value=1, max_value=118, value=5)
    if st.button("Start Quiz"):
        st.session_state.questions = data.sample(num).to_dict(orient="records")
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.results = []
        st.session_state.started = True
        st.experimental_rerun()

else:
    i = st.session_state.index
    total = len(st.session_state.questions)

    if i < total:
        row = st.session_state.questions[i]

        ask_type = random.choice(["name_to_symbol", "symbol_to_name"])
        element = row[name_col]
        symbol = row[symbol_col]

        if ask_type == "name_to_symbol":
            prompt = f"What is the symbol for {element}?"
            correct = symbol
        else:
            prompt = f"What element has the symbol {symbol}?"
            correct = element

        st.subheader(f"Question {i+1} of {total}")
        st.write(prompt)

        answer = st.text_input("Your answer:", key=f"answer_{i}")

        if st.button("Submit Answer", key=f"submit_{i}"):
            if is_close(answer, correct):
                st.success("Correct.")
                st.session_state.score += 1
                st.session_state.results.append((True, correct))
            else:
                st.error(f"Incorrect. Correct answer: {correct}")
                st.session_state.results.append((False, correct))

            st.session_state.index += 1
            st.experimental_rerun()

    else:
        st.header("Quiz Complete")
        st.write(f"Your final score: {st.session_state.score}/{total}")

        if st.checkbox("Show all answers"):
            for idx, (correct, value) in enumerate(st.session_state.results, 1):
                icon = "Correct" if correct else "Incorrect"
                st.write(f"{idx}. {value} - {icon}")

        if st.button("Play Again"):
            st.session_state.started = False
            st.experimental_rerun()
