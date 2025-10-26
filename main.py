import streamlit as st
import json
import requests
import base64

# ==============================
# CONFIGURAÇÕES GITHUB
# ==============================
REPO_OWNER = "SEU_USUARIO"
REPO_NAME = "SEU_REPO"
FILE_PATH = "questions.json"

RAW_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{FILE_PATH}"
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
TOKEN = st.secrets["GH_TOKEN"]  # configure no Streamlit Secrets


# ==============================
# FUNÇÕES
# ==============================
@st.cache_data
def load_questions() -> dict:
    try:
        r = requests.get(RAW_URL)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"❌ Erro ao carregar JSON do GitHub: {e}")
        return {}


def save_questions(data: dict):
    try:
        # Obter SHA do arquivo atual
        res = requests.get(API_URL, headers={"Authorization": f"token {TOKEN}"})
        sha = res.json().get("sha", None)

        # JSON → base64
        encoded = base64.b64encode(
            json.dumps(data, indent=4, ensure_ascii=False).encode("utf-8")
        ).decode("utf-8")

        payload = {
            "message": "update questions ✅",
            "content": encoded,
            "sha": sha
        }

        r = requests.put(API_URL, json=payload,
                         headers={"Authorization": f"token {TOKEN}"})

        if r.status_code in (200, 201):
            st.success("✅ Arquivo atualizado com sucesso!")
            st.cache_data.clear()  # limpar cache para atualizar
        else:
            st.error(f"❌ Erro do GitHub: {r.text}")

    except Exception as e:
        st.error(f"❌ Falha ao salvar no GitHub: {e}")


# ==============================
# APP UI
# ==============================
st.title("🌍 Perguntas & Respostas")

questions = load_questions()

search = st.text_input("Pesquisar", placeholder="Digite aqui...").lower()

st.divider()

if not search:
    st.subheader("Todas as perguntas")
    for q, a in questions.items():
        st.write(f"**{q}**")
        st.write(f"{a}")
        st.write("---")

else:
    if search != "thylacocephalo is an alien":
        st.subheader(f"Resultados para: {search}")
        found = False

        for q, a in questions.items():
            if search in q.lower():
                found = True
                st.write(f"**{q}**")
                st.write(f"{a}")
                st.write("---")

        if not found:
            st.warning(f"Nenhum resultado para **{search}**")
    else:
        st.subheader("➕ Adicionar Pergunta")

        new_q = st.text_input("Pergunta")
        new_a = st.text_input("Resposta")

        if st.button("Salvar no GitHub ✅"):
            if new_q.strip():
                questions[new_q] = new_a
                save_questions(questions)
            else:
                st.warning("Preencha a pergunta!")

