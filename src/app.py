import streamlit as st
import pandas as pd
from agente import responder

st.set_page_config(page_title="FinBot", layout="wide")

st.title("💰 FinBot - Assistente Financeiro Inteligente")

# ===== CARREGAR DADOS =====
df = pd.read_csv("../data/transacoes.csv")
df.columns = df.columns.str.lower()

despesas = df[df["tipo"].str.lower() == "saida"].copy()

# ===== MÉTRICAS =====
total = despesas["valor"].sum()
maior_categoria = despesas.groupby("categoria")["valor"].sum().idxmax()
maior_valor = despesas.groupby("categoria")["valor"].sum().max()

col1, col2, col3 = st.columns(3)

col1.metric("💸 Total gasto", f"R${total:.2f}")
col2.metric("📊 Maior categoria", maior_categoria)
col3.metric("🔥 Maior valor", f"R${maior_valor:.2f}")

# ===== GRÁFICO =====
st.subheader("📊 Distribuição de gastos")

grafico = despesas.groupby("categoria")["valor"].sum()

st.bar_chart(grafico)

# pizza (mais bonito)
st.subheader("🥧 Proporção dos gastos")
st.pyplot(grafico.plot.pie(autopct='%1.1f%%').figure)

# ===== CHAT =====
st.divider()
st.subheader("💬 Converse com o FinBot")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

pergunta = st.chat_input("Digite sua pergunta...")

if pergunta:
    with st.chat_message("user"):
        st.write(pergunta)

    st.session_state.mensagens.append({"role": "user", "content": pergunta})

    resposta = responder(pergunta)

    with st.chat_message("assistant"):
        st.write(resposta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})