import streamlit as st
import pandas as pd
import os
from agente import responder

# ===== CONFIGURAÇÃO DA PÁGINA =====
st.set_page_config(
    page_title="FinBot",
    page_icon="💰",
    layout="wide"
)

st.title("💰 FinBot - Assistente Financeiro")

# ===== CARREGAR DADOS (CORRIGIDO PARA STREAMLIT CLOUD) =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
caminho = os.path.join(BASE_DIR, "..", "data", "transacoes.csv")

try:
    df = pd.read_csv(caminho)
except Exception as e:
    st.error("Erro ao carregar os dados. Verifique o caminho do arquivo.")
    st.stop()

# ===== TRATAMENTO DOS DADOS =====
df.columns = df.columns.str.lower()
df["valor"] = df["valor"].astype(float)

# separar despesas
despesas = df[df["tipo"].str.lower() == "saida"]

# ===== DASHBOARD =====
st.subheader("📊 Resumo Financeiro")

total = despesas["valor"].sum()

if not despesas.empty:
    grafico = despesas.groupby("categoria")["valor"].sum()

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(grafico)

    with col2:
        st.write("Distribuição de gastos por categoria:")
        st.pyplot(grafico.plot.pie(autopct='%1.1f%%').figure)

    maior_categoria = grafico.idxmax()
    maior_valor = grafico.max()
    percentual = (maior_valor / total) * 100

    st.info(
        f"⚠️ Você está gastando {percentual:.1f}% do seu orçamento em {maior_categoria}. "
        f"O ideal é manter abaixo de 30%."
    )
else:
    st.warning("Nenhuma despesa encontrada.")

# ===== CHAT =====
st.subheader("💬 Converse com o FinBot")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# mostrar histórico
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input
pergunta = st.chat_input("Ex: Como economizar em moradia?")

if pergunta:
    # mostrar pergunta
    with st.chat_message("user"):
        st.write(pergunta)

    st.session_state.mensagens.append({
        "role": "user",
        "content": pergunta
    })

    # gerar resposta
    resposta = responder(pergunta)

    # mostrar resposta
    with st.chat_message("assistant"):
        st.write(resposta)

    st.session_state.mensagens.append({
        "role": "assistant",
        "content": resposta
    })