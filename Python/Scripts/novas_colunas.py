import pandas as pd
import ast

# Carrega os dois arquivos
df_main = pd.read_csv("IMDBest.IMDBest.csv")
df_genres = pd.read_csv("Data/Tratados/filmes_imdb_unificado.csv")

# Merge usando Title e Year
df_merge = pd.merge(df_main, df_genres[['Title', 'Year', 'genres']], on=['Title', 'Year'], how='left')

# Função para limpar colunas string tipo lista
def clean_str_list(val):
    if pd.isna(val) or not val:
        return ''
    if isinstance(val, str) and val.strip().startswith('['):
        try:
            items = ast.literal_eval(val)
        except Exception:
            items = [g.strip() for g in val.replace('[','').replace(']','').replace("'",'').split(',')]
    else:
        items = [g.strip() for g in str(val).split(',')]
    return ', '.join([g for g in items if g])

# Limpa as colunas problemáticas
cols_to_clean = ['genres', 'writers', 'directors', 'stars', 'Languages']
for col in cols_to_clean:
    if col in df_merge.columns:
        df_merge[col] = df_merge[col].apply(clean_str_list)

# Cria a coluna 'genres_first2' limpa
def get_first_two_str(genres):
    if pd.isna(genres) or not genres:
        return ''
    items = [g.strip() for g in str(genres).split(',')]
    return ', '.join([g for g in items[:2] if g])

df_merge['genres_first2'] = df_merge['genres'].apply(get_first_two_str)

# Remove a coluna _id se existir
if '_id' in df_merge.columns:
    df_merge = df_merge.drop(columns=['_id'])

# Salva o novo CSV
df_merge.to_csv("IMDBest.IMDBest.com_generos.csv", index=False)
print("Colunas string limpas e coluna '_id' removida. 'genres_first2' criada.")