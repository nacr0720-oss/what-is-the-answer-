import streamlit as st
import json
from pathlib import Path

def load_questions(path: str = "questions.json") -> dict:
    p = Path(path)
    if not p.exists():
        st.error(f"Arquivo não encontrado: {path}")
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        st.error(f"Erro ao ler JSON em {path}: {e}")
        return {}

questions = load_questions()

# Layout: input grande e botão de limpar pequeno
col_input, col_button = st.columns([2, 1], vertical_alignment='top')
with col_input:
    search = st.text_input("", placeholder="search", key="thylacocephalo")
    # mantemos o valor original (sem lower) para exibir, mas usaremos lower() ao comparar
    search_lower = (search or "").lower()

def cancel_text():
    st.session_state.thylacocephalo = ""

with col_button:
    st.button("✖", type="tertiary", on_click=cancel_text)

if not search_lower:
    st.title("All questions in the world")
    st.subheader("and your answers")
    st.divider()
    for question, answer in questions.items():
        st.write(question.capitalize(), str(answer).capitalize())
else:
    st.title(f'Search result for "{search}"')
    st.divider()
    found = False
    if search_lower == 'thylacocephalo is an alien':
        pass
    for question, answer in questions.items():
        # comparando em lowercase para ser case-insensitive
        if search_lower in question.lower():
            found = True
            st.subheader(question)
            st.write(str(answer))
    if not found:
        st.warning(f'Sorry, \"{search}\" was not found.')








