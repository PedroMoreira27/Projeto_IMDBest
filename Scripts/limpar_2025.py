import pandas as pd

# Carrega o CSV
df = pd.read_csv("c:/Users/vbald/Projeto_IMDBest/IMDBest.IMDBest.com_generos.csv")

# Lista das colunas a limpar
cols_limpar = [
    "oscar_winner", "oscar_nominated",
    "globe_winner", "globe_nominated"
]

# Limpa apenas para filmes de 2025
df.loc[df["Year"] == 2025, cols_limpar] = None

# Salva o resultado
df.to_csv("c:/Users/vbald/Projeto_IMDBest/IMDBest.IMDBest.com_generos.csv", index=False)
print("Colunas limpas para filmes de 2025.")