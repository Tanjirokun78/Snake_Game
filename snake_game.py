import streamlit as st
import random
import time

# --- Configuration ---
st.set_page_config(page_title="🐍 Snake Game", page_icon="🕹️", layout="centered")

# 💅 Thème coloré avec CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #8A2BE2;
        background-image: linear-gradient(120deg, #4B0082 0%, #ebedee 100%);
    }
    .score-box {
        background-color: #8A2BE2;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Constantes ---
GRID_SIZE = 10
SPEED = 0.4  # secondes entre mouvements

# --- Initialisation ---
if "snake" not in st.session_state:
    st.session_state.snake = [(5, 5)]
    st.session_state.food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    st.session_state.direction = "RIGHT"
    st.session_state.score = 0
    st.session_state.high_score = 0
    st.session_state.game_over = False
    st.session_state.last_move_time = time.time()

# --- Fonctions ---
def new_food():
    while True:
        pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if pos not in st.session_state.snake:
            return pos

def move():
    head_x, head_y = st.session_state.snake[-1]
    if st.session_state.direction == "UP":
        head_y -= 1
    elif st.session_state.direction == "DOWN":
        head_y += 1
    elif st.session_state.direction == "LEFT":
        head_x -= 1
    elif st.session_state.direction == "RIGHT":
        head_x += 1

    new_head = (head_x, head_y)

    if (
        head_x < 0 or head_x >= GRID_SIZE or
        head_y < 0 or head_y >= GRID_SIZE or
        new_head in st.session_state.snake
    ):
        st.session_state.game_over = True
        return

    st.session_state.snake.append(new_head)

    if new_head == st.session_state.food:
        st.session_state.score += 1
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score
        st.session_state.food = new_food()
    else:
        st.session_state.snake.pop(0)

# --- Interface ---
st.title("🐍 Snake Game - Version Colorée")

st.markdown(f"""
<div class='score-box'>
<h4>Score actuel : {st.session_state.score}</h4>
<h5>🏆 Meilleur score : {st.session_state.high_score}</h5>
</div>
""", unsafe_allow_html=True)

# --- Grille ---
for y in range(GRID_SIZE):
    row = ""
    for x in range(35):
        cell = (x, y)
        if cell == st.session_state.food:
            row += "🍎"
        elif cell in st.session_state.snake:
            row += "🟩"
        else:
            row += "🟪"
    st.text(row)

# --- Contrôles (boutons uniquement car clavier limité) ---
if st.session_state.game_over:
    st.error("💀 Game Over !")
    if st.button("🧙‍♂️ Rejouer"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("⬅️ Gauche"):
        st.session_state.direction = "LEFT"
    if col2.button("⬆️ Haut"):
        st.session_state.direction = "UP"
    if col3.button("⬇️ Bas"):
        st.session_state.direction = "DOWN"
    if col4.button("➡️ Droite"):
        st.session_state.direction = "RIGHT"

    now = time.time()
    if now - st.session_state.last_move_time > SPEED:
        move()
        st.session_state.last_move_time = now
        st.rerun()


