import openai

client = openai.OpenAI(api_key="")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Resuma: Gastos totais R$1000, maior categoria: Alimentação"}
    ]
)
print(response.choices[0].message.content)
