import streamlit as st
import random
import numpy as np

# Game Title
st.title("Tic-Tac-Toe")
st.subheader("Win by answering questions correctly!")

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = np.full((3, 3), " ")
    st.session_state.turn = "X"
    st.session_state.winner = None
    st.session_state.selected_cell = None
    st.session_state.selected_question = None
    st.session_state.questions = {
        "What is the capital of Pakistan?": ("Islamabad", "Karachi"),
        "Who is the founder of Pakistan?": ("Quaid-e-Azam Muhammad Ali Jinnah", "Allama Iqbal"),
        "What is the national language of Pakistan?": ("Urdu", "Punjabi"),
        "Which year did Pakistan gain independence?": ("1947", "1956"),
        "What is the national sport of Pakistan?": ("Field Hockey", "Cricket"),
        "Which is the highest peak in Pakistan?": ("K2", "Nanga Parbat"),
    }


# Function to check for a winner
def check_winner():
    board = st.session_state.board
    for i in range(3):
        if np.all(board[i, :] == board[i, 0]) and board[i, 0] != " ":
            return board[i, 0]
        if np.all(board[:, i] == board[0, i]) and board[0, i] != " ":
            return board[0, i]
    if board[0, 0] == board[1, 1] == board[2, 2] and board[0, 0] != " ":
        return board[0, 0]
    if board[0, 2] == board[1, 1] == board[2, 0] and board[0, 2] != " ":
        return board[0, 2]
    if " " not in board:
        return "Tie"
    return None


# Display current turn
st.write(f"**Current Turn: Player {st.session_state.turn}**")

# Display the board
st.write("### Game Board")
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        if cols[j].button(st.session_state.board[i, j], key=f"{i}-{j}") and st.session_state.board[
            i, j] == " " and not st.session_state.winner:
            # Store selected cell
            st.session_state.selected_cell = (i, j)
            st.session_state.selected_question = random.choice(list(st.session_state.questions.items()))
            st.rerun()

# Show the question if a cell was selected
if st.session_state.selected_question:
    question, (correct, wrong) = st.session_state.selected_question
    st.write(f"**Question:** {question}")

    if st.button(correct, key="correct_answer"):
        i, j = st.session_state.selected_cell
        st.session_state.board[i, j] = st.session_state.turn
        st.session_state.turn = "O" if st.session_state.turn == "X" else "X"
        st.session_state.selected_cell = None
        st.session_state.selected_question = None
        st.session_state.winner = check_winner()
        st.rerun()

    if st.button(wrong, key="wrong_answer"):
        st.write("Wrong answer! The AI gets a free move.")
        st.session_state.turn = "O" if st.session_state.turn == "X" else "X"
        st.session_state.selected_cell = None
        st.session_state.selected_question = None
        st.rerun()

# Show winner
if st.session_state.winner:
    if st.session_state.winner == "Tie":
        st.info("It's a tie! 🤝")
    else:
        st.success(f"{st.session_state.winner} wins! 🎉")
    if st.button("Play Again"):
        st.session_state.board = np.full((3, 3), " ")
        st.session_state.turn = "X"
        st.session_state.winner = None
        st.session_state.selected_cell = None
        st.session_state.selected_question = None
        st.rerun()
