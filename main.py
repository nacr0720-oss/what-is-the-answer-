import streamlit as st
import json
from pathlib import Path
from time import sleep

def load_questions(path: str = "questions.json") -> dict:
    p = Path(path)
    if not p.exists():
        st.error(f"Arquivo não encontrado: {path}")
        return {}
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        st.error(f"Erro ao ler JSON em {path}: {e}")
        return {}

questions = load_questions()

# Layout: input grande e botão de limpar pequeno
col_input, col_button = st.columns([3, 1])

with col_button:
    st.button("✖", type="tertiary", on_click=cancel_text)
    
with col_input:
    st.subheader('try look to end')
    search = st.text_input("", placeholder="search", key="thylacocephallo")
    # mantemos o valor original (sem lower) para exibir, mas usaremos lower() ao comparar
    search_lower = (search or "").lower()

def cancel_text():
    st.session_state.thylacocephallo = ""

if not search_lower:
    st.title("All questions in the world")
    st.subheader("and your answers")
    st.divider()
    for question, answer in questions.items():
        st.write(str(question) + str(answer))
else:
    st.title(f'Search result for "{search}"')
    st.divider()
    found = False
    for question, answer in questions.items():
        # comparando em lowercase para ser case-insensitive
        if search_lower in question.lower():
            found = True
            st.subheader(question)
            st.write(str(answer))
        elif search == 't h a sanc':
            found = True
            st.subheader('@NACRIT0')
            st.write('https://www.youtube.com/watch?v=hPr-Yc92qaY')
            sleep(5)
            st.error('in the comments')
            sleep(0.5)
            cancel_text()
        elif search == 'B obctme':
            found = True
            st.write('https://youtu.be/_koeuijFOEU')
        elif search.lower() == 'silksong':
            st.write('yes... song not a spectogram... https://www.mediafire.com/file/89f2x7nd29srjg5/end.mp3/file')
        elif search == 'sanc':
            st.markdown('**:rainbow[thylacocephalo]**')
    if not found:
        st.warning(f'Sorry, \"{search}\" was not found.')
        sleep(60)
        st.write('please look too end')






















