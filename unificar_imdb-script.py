import os
import pandas as pd

# Caminho relativo para a pasta com os arquivos CSV
caminho_pasta = os.path.join('Data', 'IMDB')

# Lista para armazenar os DataFrames
lista_df = []

for ano in range(1920, 2026):
    nome_arquivo = f"merged_movies_data_{ano}.csv"
    caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)

    try:
        df = pd.read_csv(caminho_arquivo)

        # Corrige a primeira coluna (nome dos filmes), mantendo o nome da coluna original
        primeira_coluna = df.columns[0]
        df[primeira_coluna] = df[primeira_coluna].str.replace(r'^\d+\.\s*', '', regex=True)

        lista_df.append(df)
    except Exception as e:
        print(f"Erro ao ler {nome_arquivo}: {e}")

# Junta todos os DataFrames
df_final = pd.concat(lista_df, ignore_index=True)

# Salva no CSV final
df_final.to_csv('filmes_imdb_unificado.csv', index=False)
print("Arquivo unificado criado com sucesso: filmes_imdb_unificado.csv")