import streamlit as st
import pd as pd
import time

# --- 1. Custom CSS for Uniform "Blue Graph" TV Look ---
st.markdown("""
<style>
    .stApp { background-color: #000033; }
    h3 {
        color: #FFCC00 !important;
        text-align: center;
        text-transform: uppercase;
        font-family: 'Arial Black', Gadget, sans-serif;
        text-shadow: 2px 2px #000000;
        min-height: 120px !important; 
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem !important;
        margin-bottom: 20px !important;
    }
    .stButton > button {
        background-color: #060ce9 !important;
        color: #FFCC00 !important;
        border: 3px solid #FFCC00 !important;
        height: 100px !important;
        width: 100% !important;
        font-size: 32px !important;
        font-weight: bold !important;
        border-radius: 5px !important;
    }
    .stButton > button:hover { border-color: #FFFFFF !important; color: #FFFFFF !important; }
    .stButton > button:disabled { background-color: #000022 !important; color: #444444 !important; border: 2px solid #222222 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #060ce9; padding: 10px; }
    .stTabs [data-baseweb="tab"] { color: white !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 2. Load School Edition Data ---
@st.cache_data
def load_data():
    return pd.DataFrame([
        # Math
        {"Category": "Math", "Points": 100, "Question": "100 * 100", "Answer": "What is 10,000?"},
        {"Category": "Math", "Points": 200, "Question": "3x - 73 = 200", "Answer": "What is 91?"},
        {"Category": "Math", "Points": 300, "Question": "Name the graph of y = x", "Answer": "What is a linear equation/line?"},
        {"Category": "Math", "Points": 400, "Question": "Find the derivative of x^2", "Answer": "What is 2x?"},
        {"Category": "Math", "Points": 500, "Question": "What is an integral?", "Answer": "What is the area under a curve/anti-derivative?"},
        # English
        {"Category": "English", "Points": 100, "Question": "The main idea of a passage or paragraph", "Answer": "What is the central point/theme?"},
        {"Category": "English", "Points": 200, "Question": "A figure of speech that directly compares two unrelated things", "Answer": "What is a metaphor?"},
        {"Category": "English", "Points": 300, "Question": "Name a literary device", "Answer": "What is a simile / metaphor?"},
        {"Category": "English", "Points": 400, "Question": "Who wrote Romeo and Juliet?", "Answer": "Who is William Shakespeare?"},
        {"Category": "English", "Points": 500, "Question": "How is an Essay written?", "Answer": "What is Introduction, Body, and Conclusion?"},
        # History
        {"Category": "History", "Points": 100, "Question": "When was Jesus born?", "Answer": "What is 4 BC?"},
        {"Category": "History", "Points": 200, "Question": "This country was the foundation of democracy", "Answer": "What is Ancient Greece?"},
        {"Category": "History", "Points": 300, "Question": "This person was known for unifying all of China", "Answer": "Who is Qin Shi Huang?"},
        {"Category": "History", "Points": 400, "Question": "When did the American Revolution happen?", "Answer": "What is 1775?"},
        {"Category": "History", "Points": 500, "Question": "Who did the Roman Empire begin with?", "Answer": "Who is Augustus Caesar?"},
        # Science
        {"Category": "Science", "Points": 100, "Question": "What is the closest planet to the Sun?", "Answer": "What is Mercury?"},
        {"Category": "Science", "Points": 200, "Question": "What is the powerhouse of the cell?", "Answer": "What is the mitochondria?"},
        {"Category": "Science", "Points": 300, "Question": "What is the chemical symbol for gold?", "Answer": "What is Au?"},
        {"Category": "Science", "Points": 400, "Question": "What force keeps us on the ground?", "Answer": "What is gravity?"},
        {"Category": "Science", "Points": 500, "Question": "What is the hardest natural substance on Earth?", "Answer": "What is a diamond?"},
        # Coding
        {"Category": "Coding", "Points": 100, "Question": "Name a base language of programming", "Answer": "What is C/Assembly/Python/Java/Rust?"},
        {"Category": "Coding", "Points": 200, "Question": "Which language is most popular?", "Answer": "What is Python/JavaScript?"},
        {"Category": "Coding", "Points": 300, "Question": "What is an array?", "Answer": "What is programming storage?"},
        {"Category": "Coding", "Points": 400, "Question": "What does OOP stand for?", "Answer": "What is Object-Oriented Programming?"},
        {"Category": "Coding", "Points": 500, "Question": "What type of language is ARM?", "Answer": "What is Machine Language/Assembly"}
    ])

df = load_data()
categories = df['Category'].unique()

# --- 3. Session State ---
if "players" not in st.session_state:
    st.session_state.update({
        "players": {}, "answered": [], "current_q": None, 
        "show_answer": False, "final_triggered": False, 
        "final_q_revealed": False, "final_a_revealed": False, "winner": None
    })

# --- 4. Sidebar ---
with st.sidebar:
    st.title("Host Admin")
    new_p = st.text_input("Player Name")
    if st.button("Add Player") and new_p:
        st.session_state.players[new_p] = 0
        st.rerun()
    st.divider()
    if not st.session_state.final_triggered:
        if st.button("🔥 FINAL JEOPARDY", type="primary"):
            st.session_state.final_triggered = True
            st.rerun()
    else:
        if st.button("↩️ BOARD"):
            st.session_state.final_triggered = False
            st.session_state.final_q_revealed = False
            st.session_state.final_a_revealed = False
            st.rerun()
    if st.button("Reset All"):
        st.session_state.clear()
        st.rerun()

# --- 5. Tabs ---
tab1, tab2 = st.tabs(["🎮 GAME BOARD", "🏆 LEADERBOARD"])

with tab1:
    if st.session_state.winner:
        st.balloons()
        st.title(f"🥇 THE WINNER IS {st.session_state.winner.upper()}!")
        if st.button("Back to Game"):
            st.session_state.winner = None
            st.rerun()

    elif st.session_state.final_triggered:
        st.title("🏆 FINAL JEOPARDY")
        st.markdown("### Category: General Knowledge")
        if not st.session_state.final_q_revealed:
            if st.button("REVEAL FINAL QUESTION", use_container_width=True):
                st.session_state.final_q_revealed = True
                st.rerun()
        if st.session_state.final_q_revealed:
            st.warning("### What is a u-boat?")
            if not st.session_state.final_a_revealed:
                if st.button("REVEAL FINAL ANSWER"):
                    st.session_state.final_a_revealed = True
                    st.rerun()
            if st.session_state.final_a_revealed:
                st.success("### Answer: What is a German submarine?")
                st.balloons()
    
    elif st.session_state.current_q is None:
        cols = st.columns(len(categories))
        for i, cat in enumerate(categories):
            with cols[i]:
                st.markdown(f"### {cat}")
                cat_qs = df[df['Category'] == cat].sort_values('Points')
                for _, row in cat_qs.iterrows():
                    q_id = f"{cat}-{row['Points']}"
                    if q_id in st.session_state.answered:
                        st.button("X", key=q_id, disabled=True)
                    else:
                        if st.button(f"${row['Points']}", key=q_id):
                            st.session_state.current_q = row
                            st.rerun()
    else:
        q = st.session_state.current_q
        st.info(f"{q['Category']} - ${q['Points']}")
        st.markdown(f"## {q['Question']}")
        
        if not st.session_state.show_answer:
            if st.button("REVEAL ANSWER", use_container_width=True):
                st.session_state.show_answer = True
                st.rerun()
        else:
            st.success(f"### {q['Answer']}")
            st.write("---")
            st.write("### Assign Points")
            
            if not st.session_state.players:
                st.error("No players found! Please add players in the sidebar.")
            else:
                p_names = list(st.session_state.players.keys())
                p_cols = st.columns(len(p_names))
                for i, name in enumerate(p_names):
                    with p_cols[i]:
                        st.markdown(f"<p style='color:#FFCC00; text-align:center; font-weight:bold; font-size:20px;'>{name}</p>", unsafe_allow_html=True)
                        col_correct, col_wrong = st.columns(2)
                        if col_correct.button("✅", key=f"c_{name}"):
                            st.session_state.players[name] += q['Points']
                            st.balloons()
                            time.sleep(1) 
                            st.session_state.answered.append(f"{q['Category']}-{q['Points']}")
                            st.session_state.current_q, st.session_state.show_answer = None, False
                            st.rerun()
                        if col_wrong.button("❌", key=f"w_{name}"):
                            st.session_state.players[name] -= q['Points']
                            st.snow()
                            time.sleep(1)
                            st.rerun()
            
            if st.button("Skip Question"):
                st.session_state.answered.append(f"{q['Category']}-{q['Points']}")
                st.session_state.current_q, st.session_state.show_answer = None, False
                st.rerun()

with tab2:
    st.header("Current Rankings")
    if st.session_state.players:
        sorted_p = dict(sorted(st.session_state.players.items(), key=lambda item: item[1], reverse=True))
        for name, score in sorted_p.items():
            c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1.5])
            c1.markdown(f"## {name}")
            c2.markdown(f"## ${score}")
            if c3.button("+$100", key=f"add_{name}"): st.session_state.players[name] += 100; st.rerun()
            if c4.button("-$100", key=f"sub_{name}"): st.session_state.players[name] -= 100; st.rerun()
            if c5.button("🏆 WINNER", key=f"win_{name}"):
                st.session_state.winner = name
                st.rerun()
            st.divider()
    else:
        st.info("Add players in the sidebar to start.")