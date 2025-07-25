from fpdf import FPDF
from datetime import datetime

def exportar_pdf(dados, insight, receita, grafico_cat="grafico_categoria.png", grafico_mes="grafico_mes.png", nome_arquivo="relatorio_gastos.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Relatório Inteligente de Gastos Pessoais", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Data do Relatório: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    # Receita
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Receita mensal: R$ {receita:,.2f}", ln=True)
    pdf.ln(5)

    # Gráfico por Categoria
    if grafico_cat:
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(200, 10, txt="Gráfico: Gasto por Categoria", ln=True)
        pdf.image(grafico_cat, x=10, w=pdf.w - 20)
        pdf.ln(8)

    # Gráfico por Mês
    if grafico_mes:
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(200, 10, txt="Gráfico: Gasto por Mês", ln=True)
        pdf.image(grafico_mes, x=10, w=pdf.w - 20)
        pdf.ln(8)

    # Resumo dos gastos
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(200, 10, txt="Resumo dos Gastos", ln=True)
    pdf.set_font("Arial", size=10)
    total = dados['valor'].sum()
    pdf.cell(200, 8, txt=f"Gasto total: R$ {total:,.2f}", ln=True)
    pdf.ln(2)
    pdf.cell(200, 8, txt="Top 3 categorias:", ln=True)
    top3 = dados.groupby('categoria')['valor'].sum().sort_values(ascending=False).head(3)
    for cat, val in top3.items():
        pdf.cell(200, 7, txt=f"  - {cat}: R$ {val:,.2f}", ln=True)
    pdf.ln(5)

    # Insight IA
    if insight:
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(200, 10, txt="Insight Inteligente", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 6, insight)
        pdf.ln(5)

    pdf.output(nome_arquivo)
    return nome_arquivo
