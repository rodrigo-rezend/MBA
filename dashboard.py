import streamlit as st
import pandas as pd
from ia_insights import gerar_insight
from pdf_utils import exportar_pdf
import matplotlib.pyplot as plt

## Disciplina de bigData MBA - Projeto de Análise de Gastos Pessoais

def salvar_grafico_categoria(gastos, path="grafico_categoria.png"):
    cat = gastos.groupby('categoria')['valor'].sum().sort_values(ascending=False)
    plt.figure(figsize=(6, 3))
    cat.plot(kind='bar')
    plt.title("Gasto por Categoria")
    plt.ylabel("Valor (R$)")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def salvar_grafico_mes(gastos, path="grafico_mes.png"):
    gastos['data'] = pd.to_datetime(gastos['data'])
    gastos['mes'] = gastos['data'].dt.to_period('M').astype(str)
    mes = gastos.groupby('mes')['valor'].sum()
    plt.figure(figsize=(6, 3))
    mes.plot(kind='line', marker='o')
    plt.title("Gasto por Mês")
    plt.ylabel("Valor (R$)")
    plt.xlabel("Mês")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

st.set_page_config(page_title="Painel de Gastos Pessoais", layout="wide")
st.title("Painel Inteligente de Gastos Pessoais")

# 1. Download do exemplo de planilha
st.markdown("#### Baixe um exemplo de planilha para importar seus próprios gastos:")
exemplo = pd.DataFrame({
    "data": ["2025-07-10", "2025-07-10"],
    "categoria": ["Alimentação", "Transporte"],
    "valor": [50.0, 35.0],
    "descricao": ["Almoço no restaurante", "Uber para o trabalho"],
    "forma_pagamento": ["Crédito", "Débito"]
})
st.download_button(
    label="📥 Baixar exemplo de planilha (CSV)",
    data=exemplo.to_csv(index=False),
    file_name="gastos_exemplo.csv",
    mime="text/csv"
)

# 2. Upload do arquivo do usuário
st.markdown("#### Faça upload da sua planilha de gastos pessoais:")
uploaded_file = st.file_uploader("Escolha um arquivo CSV no mesmo formato do exemplo", type="csv")

if uploaded_file is not None:
    try:
        gastos = pd.read_csv(uploaded_file)
        st.success("Planilha carregada com sucesso!")
        st.dataframe(gastos.head(20), use_container_width=True)

        # 3. Pergunta a receita mensal
        st.markdown("#### Informe sua receita mensal para uma análise financeira personalizada:")
        receita = st.number_input("Receita mensal (R$)", min_value=0.0, step=0.01, format="%.2f")

        # 4. Bloco de IA de insights (imediatamente abaixo da receita)
        st.header("💡 Insights Inteligentes com IA")
        tipo_insight = st.selectbox(
            "O que você deseja saber?",
            [
                "Resumo geral dos meus gastos",
                "Quais categorias estou gastando mais?",
                "Dicas para economizar com base nos meus gastos",
                "Avaliação de possíveis gastos excessivos",
                "Gerar alerta sobre padrão fora do comum"
            ]
        )

        botao = st.button("Gerar Insight com IA", disabled=(receita <= 0))
        if botao and receita > 0:
            with st.spinner("Gerando insight com IA, aguarde..."):
                insight = gerar_insight(gastos, tipo_insight, receita)
                st.session_state["insight_ia"] = insight  # <-- salva o insight na sessão
                st.markdown(insight)
        elif receita <= 0:
            st.info("Preencha sua receita mensal para liberar a geração de insights.")

        # Exibe insight salvo, botão PDF e exportação
        if "insight_ia" in st.session_state and st.session_state["insight_ia"]:
            insight = st.session_state["insight_ia"]
            st.markdown(insight)
            # Salve gráficos antes de exportar
            salvar_grafico_categoria(gastos, "grafico_categoria.png")
            salvar_grafico_mes(gastos, "grafico_mes.png")
            st.markdown("---")
            if st.button("📄 Exportar Relatório em PDF"):
                arquivo_pdf = exportar_pdf(
                    gastos, insight, receita,
                    grafico_cat="grafico_categoria.png",
                    grafico_mes="grafico_mes.png"
                )
                with open(arquivo_pdf, "rb") as f:
                    st.download_button(
                        label="Clique aqui para baixar o relatório em PDF",
                        data=f,
                        file_name=arquivo_pdf,
                        mime="application/pdf"
                    )

        # 5. Visualizações e Métricas
        st.header("🔎 Visão Geral dos Gastos")
        st.metric("Gasto total", f'R$ {gastos["valor"].sum():,.2f}')

        st.subheader("Gasto por Categoria")
        cat = gastos.groupby('categoria')['valor'].sum().sort_values(ascending=False)
        st.bar_chart(cat)

        st.subheader("Top 5 Maiores Gastos")
        top5 = gastos.sort_values(by='valor', ascending=False).head(5)
        st.dataframe(top5, use_container_width=True)

        # Gráfico por mês
        try:
            gastos['data'] = pd.to_datetime(gastos['data'])
            gastos['mes'] = gastos['data'].dt.to_period('M').astype(str)
            gastos_mes = gastos.groupby('mes')['valor'].sum()
            st.subheader("Gasto por Mês")
            st.line_chart(gastos_mes)
        except Exception:
            st.warning("Não foi possível processar as datas. Verifique o formato da coluna 'data'.")

    except Exception as e:
        st.error(f"Erro ao ler ou processar o arquivo: {e}")

else:
    st.info("Faça upload da sua planilha de gastos pessoais para iniciar a análise. Se preferir, use o modelo de exemplo.")
