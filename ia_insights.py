import openai
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Prompt especialista financeiro
system_prompt = (
    "Você é um consultor financeiro pessoal, especialista em finanças pessoais, didático, amigável e objetivo. "
    "Sua missão é analisar uma tabela de gastos fornecida pelo usuário junto com o valor da receita mensal. "
    "Faça análises inteligentes, destaque padrões relevantes, compare percentuais do orçamento, sugira dicas práticas para saúde financeira "
    "e sempre explique de forma clara e personalizada, mesmo se os valores forem baixos. "
    "Evite repetir informações desnecessárias e traga recomendações acionáveis, como um verdadeiro consultor humano. "
    "Se faltar dados importantes (como receita ou mais categorias), oriente o usuário sobre como enriquecer a análise."
    "Formate sempre todos os valores em reais, use vírgula como separador decimal, evite colar frases, traga percentuais e, se possível, organize os pontos mais importantes em tópicos."
)

def gerar_insight(gastos_df, tipo_insight, receita, modelo="gpt-3.5-turbo"):
    api_key = os.getenv("openai_api_key")
    client = openai.OpenAI(api_key=api_key)

    # Monta o prompt de usuário conforme seleção
    receita_msg = f"Minha receita mensal é de R$ {receita:.2f}. "
    if tipo_insight == "Resumo geral dos meus gastos":
        prompt = receita_msg + (
            "Me dê um resumo dos meus gastos totais, principais categorias e meses mais críticos com base nos dados a seguir:\n"
            f"{gastos_df.to_string(index=False)}"
        )
    elif tipo_insight == "Quais categorias estou gastando mais?":
        prompt = receita_msg + (
            "Analise os dados e me diga em linguagem simples quais categorias mais consomem meu orçamento mensal, trazendo porcentagens e dicas:\n"
            f"{gastos_df.to_string(index=False)}"
        )
    elif tipo_insight == "Dicas para economizar com base nos meus gastos":
        prompt = receita_msg + (
            "Veja meus gastos abaixo e me dê dicas práticas para economizar, apontando exemplos de cortes, alternativas e sugestões para melhor saúde financeira:\n"
            f"{gastos_df.to_string(index=False)}"
        )
    elif tipo_insight == "Avaliação de possíveis gastos excessivos":
        prompt = receita_msg + (
            "Avalie os dados e aponte onde há gastos excessivos em relação à minha receita mensal, sugerindo limites e justificando:\n"
            f"{gastos_df.to_string(index=False)}"
        )
    else:
        prompt = receita_msg + (
            "Veja meus gastos abaixo e gere um alerta caso algum padrão de gasto esteja fora do comum para um orçamento pessoal:\n"
            f"{gastos_df.to_string(index=False)}"
        )

    try:
        response = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=450,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao gerar insight: {e}"
