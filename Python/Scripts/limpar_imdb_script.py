import pandas as pd

# Carrega o CSV unificado
df = pd.read_csv('filmes_imdb_unificado.csv')

# Lista de colunas que serão removidas
colunas_remover = [
    'budget',
    'opening_weekend_Gross',
    'grossWorldWWide',
    'gross_US_Canada',
    'release_date',
    'countries_origin',
    'filming_locations',
    'production_company',
    'awards_content',
    'genres'
]

# Remove as colunas (ignora se alguma não existir)
df_limpo = df.drop(columns=[col for col in colunas_remover if col in df.columns])

# Salva em um novo arquivo CSV
df_limpo.to_csv('filmes_imdb_limpo.csv', index=False)

print("Arquivo salvo como 'filmes_imdb_limpo.csv'")
