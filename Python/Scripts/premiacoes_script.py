import pandas as pd

# Carrega o dataset principal
df_filmes = pd.read_csv('filmes_imdb_limpo.csv')

# Padroniza o título do filme para facilitar a comparação
df_filmes['title_clean'] = df_filmes['Title'].str.strip().str.lower()

# Carrega os datasets de premiações
oscars_df = pd.read_csv('Data/the_oscar_award.csv')
globes_df = pd.read_csv('Data/Golden_Globes_Awards_Dataset.csv')

# Padroniza os nomes e categorias
oscars_df['film_clean'] = oscars_df['film'].astype(str).str.strip().str.lower()
oscars_df['category_clean'] = oscars_df['category'].str.upper().str.strip()

globes_df['title_clean'] = globes_df['title'].astype(str).str.strip().str.lower()
globes_df['category_clean'] = globes_df['award'].str.upper().str.strip()

# Categorias consideradas
categorias_oscar = ['BEST PICTURE', 'BEST MOTION PICTURE', 'INTERNATIONAL FEATURE FILM']
categorias_globo = [
    'BEST MOTION PICTURE - DRAMA',
    'BEST MOTION PICTURE - MUSICAL OR COMEDY',
    'BEST MOTION PICTURE - FOREIGN LANGUAGE'
]

# Função para verificar indicações e vitórias
def verificar_premiacoes(row):
    title = row['title_clean']
    
    # OSCAR
    indicacoes_oscar = oscars_df[
        (oscars_df['film_clean'] == title) &
        (oscars_df['category_clean'].isin(categorias_oscar))
    ]
    row['oscar_nominated'] = not indicacoes_oscar.empty
    row['oscar_winner'] = any(indicacoes_oscar['winner'] == True)
    row['oscar_category'] = ', '.join(indicacoes_oscar['category_clean'].unique()) if not indicacoes_oscar.empty else None

    # GLOBO DE OURO
    indicacoes_globo = globes_df[
        (globes_df['title_clean'] == title) &
        (globes_df['category_clean'].isin(categorias_globo))
    ]
    row['globe_nominated'] = not indicacoes_globo.empty
    row['globe_winner'] = any(indicacoes_globo['winner'].astype(str).str.upper() == 'TRUE')
    row['globe_category'] = ', '.join(indicacoes_globo['category_clean'].unique()) if not indicacoes_globo.empty else None

    return row

# Aplica a verificação para cada filme
df_final = df_filmes.apply(verificar_premiacoes, axis=1)

# Remove coluna auxiliar
df_final.drop(columns=['title_clean'], inplace=True)

# Salva em novo CSV
df_final.to_csv('filmes_imdb_com_premiacoes.csv', index=False)

print("Arquivo final salvo como 'filmes_imdb_com_premiacoes.csv'")
print("Premiações verificadas e adicionadas com sucesso.")