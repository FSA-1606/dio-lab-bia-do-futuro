import pandas as pd
import unicodedata

# ===== NORMALIZAR TEXTO (remove acento) =====
def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto


# ===== CARREGAR DADOS =====
def carregar_dados():
    import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
caminho = os.path.join(BASE_DIR, "..", "data", "transacoes.csv")

df = pd.read_csv(caminho)
    df.columns = df.columns.str.lower()

    # pegar só despesas
    despesas = df[df["tipo"].str.lower() == "saida"].copy()

    despesas["valor"] = despesas["valor"].astype(float)

    return despesas


# ===== FUNÇÃO PRINCIPAL =====
def responder(pergunta):
    df = carregar_dados()

    if df.empty:
        return "Não encontrei despesas nos dados."

    total = df["valor"].sum()

    # agrupar por categoria
    gastos_categoria = df.groupby("categoria")["valor"].sum()

    maior = gastos_categoria.idxmax()
    valor_maior = gastos_categoria.max()

    pergunta_norm = normalizar(pergunta)

    # detectar categoria na pergunta
    categorias = df["categoria"].unique()
    categoria_encontrada = None

    for cat in categorias:
        if normalizar(cat) in pergunta_norm:
            categoria_encontrada = cat
            break

    # palavras-chave
    palavras_total = ["gastei", "gastos", "total"]
    palavras_maior = ["maior", "mais"]
    palavras_economia = ["economizar", "reduzir", "diminuir", "cortar"]
    palavras_analise = ["analise", "resumo", "comportamento"]

    # ===== RESPOSTAS =====

    # total gasto
    if any(p in pergunta_norm for p in palavras_total):
        return f"Você gastou R${total:.2f} no total."

    # maior gasto
    elif any(p in pergunta_norm for p in palavras_maior):
        return f"Sua maior despesa é {maior}, totalizando R${valor_maior:.2f}."

    # economia inteligente
    elif any(p in pergunta_norm for p in palavras_economia):
        if categoria_encontrada:
            gasto_categoria = gastos_categoria[categoria_encontrada]
            percentual = (gasto_categoria / total) * 100

            return (
                f"Você gastou R${gasto_categoria:.2f} com {categoria_encontrada}, "
                f"o que representa {percentual:.1f}% dos seus gastos.\n\n"
                f"Para economizar nessa categoria, você pode:\n"
                f"- Revisar contratos ou serviços\n"
                f"- Buscar opções mais baratas\n"
                f"- Reduzir custos relacionados a {categoria_encontrada}"
            )
        else:
            return (
                f"Sua maior despesa é {maior}.\n"
                f"Comece reduzindo essa categoria para ter maior impacto no seu orçamento."
            )

    # análise geral
    elif any(p in pergunta_norm for p in palavras_analise):
        return (
            f"Seu maior gasto está em {maior}, representando uma parte relevante do seu orçamento.\n"
            f"Recomendo revisar essa categoria para melhorar sua saúde financeira."
        )

    return "Posso te ajudar com análise de gastos, economia ou planejamento financeiro."