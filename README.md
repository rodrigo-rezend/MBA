# Painel Inteligente de Gastos Pessoais

Este projeto demonstra, de forma prática, o uso de **processamento distribuído com PySpark** para análise de dados financeiros pessoais. Desenvolvido como atividade para a disciplina de Big Data & Hadoop, o sistema realiza ingestão, transformação e agregação de dados via Spark, preparando-os para visualização interativa em Streamlit.



## Funcionalidades
- Upload de planilhas de gastos (CSV)
- Processamento dos dados com PySpark: agregação, limpeza e análise por categoria/mês
- Visualização dos resultados em gráficos interativos (Streamlit)
- Input de receita mensal e análise personalizada com IA (OpenAI)
- Geração de relatório financeiro completo em PDF

  ![BigData](https://github.com/user-attachments/assets/3cfdec11-2a61-4b68-b38c-06009fa30553)

## Tecnologias Utilizadas

- **PySpark**: processamento distribuído
- **Pandas**: manipulação complementar de dados
- **Streamlit**: visualização web interativa
- **OpenAI GPT**: geração de insights automáticos
- **FPDF & Matplotlib**: geração de gráficos e relatórios PDF

## Como executar

1. Instale as dependências do projeto (requirements.txt)
2. Suba a aplicação com `streamlit run dashboard.py`
3. Importe sua planilha de gastos e informe a receita mensal
4. Explore gráficos, métricas e gere relatórios com insights personalizados

## Observação

Para usar a geração de insights via IA, é necessário configurar sua chave OpenAI no arquivo `.env` (não versionado).

---

Projeto desenvolvido para fins acadêmicos – MBA Big Data & Hadoop.
