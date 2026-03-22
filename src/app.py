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

st.success("🤖 Olá! Sou seu assistente financeiro. Posso analisar seus gastos e te ajudar a economizar.")

# ===== CARREGAR DADOS (CORRIGIDO PARA NUVEM) =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
caminho = os.path.join(BASE_DIR, "..", "data", "transacoes.csv")

try:
    df = pd.read_csv(caminho)
except Exception:
    st.error("Erro ao carregar os dados. Verifique o arquivo transacoes.csv.")
    st.stop()

# ===== TRATAMENTO =====
df.columns = df.columns.str.lower()
df["valor"] = df["valor"].astype(float)

despesas = df[df["tipo"].str.lower() == "saida"]

# ===== DASHBOARD =====
st.subheader("📊 Resumo Financeiro")

if not despesas.empty:
    total = despesas["valor"].sum()
    grafico = despesas.groupby("categoria")["valor"].sum()

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(grafico)

    with col2:
        st.write("Distribuição de gastos:")
        fig = grafico.plot.pie(autopct='%1.1f%%').figure
        st.pyplot(fig)

    # INSIGHT
    maior_categoria = grafico.idxmax()
    maior_valor = grafico.max()
    percentual = (maior_valor / total) * 100

    st.success(
        f"💡 Insight: Você está gastando {percentual:.1f}% em {maior_categoria}. "
        f"O ideal é manter abaixo de 30%."
    )

else:
    st.warning("Nenhuma despesa encontrada.")

# ===== TABELA DETALHADA =====
st.subheader("📋 Detalhamento dos gastos")
st.dataframe(despesas)

# ===== CHAT =====
st.subheader("💬 Converse com o FinBot")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# histórico
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

    # resposta
    resposta = responder(pergunta)

    with st.chat_message("assistant"):
        st.write(resposta)

    st.session_state.mensagens.append({
        "role": "assistant",
        "content": resposta
    })