# Pegar a base de dados x
# Ler a base de dados x
# Pegar dados da base
# Abrir o sistema botnext CRM
# Adiciona a informação na caixa de busca
# Localizamos o card no cambam e clicamos nele
# Clicamos em excluir
# Loop


import pandas as pd
import playwright as pw

df = pd.read_excel("Dados/Excluir BOT.xlsx")

#for dado in df:
df.loc["Código"]