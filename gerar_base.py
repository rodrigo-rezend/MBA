import pandas as pd
import random
from faker import Faker

fake = Faker('pt_BR')

categorias = ['Alimentação', 'Transporte', 'Lazer', 'Saúde', 'Educação', 'Compras', 'Moradia']
formas_pagamento = ['Crédito', 'Débito', 'Dinheiro', 'Pix']

dados = []

for _ in range(200):
    data = fake.date_between(start_date='-4M', end_date='today')
    categoria = random.choice(categorias)
    valor = round(random.uniform(15, 800), 2)
    descricao = fake.sentence(nb_words=4)
    forma = random.choice(formas_pagamento)
    dados.append([data, categoria, valor, descricao, forma])

df = pd.DataFrame(dados, columns=['data', 'categoria', 'valor', 'descricao', 'forma_pagamento'])
df['data'] = pd.to_datetime(df['data']).dt.strftime('%Y-%m-%d')
df.to_csv('data/gastos_pessoais.csv', index=False)
print("Arquivo gerado com sucesso!")
