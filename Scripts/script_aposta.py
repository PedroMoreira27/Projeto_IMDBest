import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from xgboost import XGBClassifier
import joblib

# 1. Carregar o dataset de apostas (filmes lançados após a última premiação)
df = pd.read_csv("IMDBest.IMDBest.com_generos.csv")

# 2. Filtrar apenas filmes SEM resultado de premiação (não supervisionado)
df_aposta = df[(df['oscar_winner'].isna()) & (df['oscar_nominated'].isna())].copy()

if df_aposta.empty:
    print("Nenhum filme novo encontrado para aposta (todos já possuem resultado de premiação).")
    exit()

# 3. Definir colunas por tipo (ajuste conforme seu pipeline de treino)
numeric_features = ['Year', 'Duration', 'Rating', 'Votes']

# Garante que a coluna existe e preenche nulos
if 'genres_first2' not in df_aposta.columns:
    raise ValueError("A coluna 'genres_first2' não existe no arquivo CSV.")

df_aposta['genres_first2'] = df_aposta['genres_first2'].fillna('')

# Split seguro para duas colunas, mesmo se estiver vazio
split_genres = df_aposta['genres_first2'].str.split(',', n=1, expand=True)

# Se não houver nenhuma coluna (todos vazios), crie duas colunas vazias
if split_genres.shape[1] == 0:
    split_genres = pd.DataFrame({'genre1': ['unknown'] * len(df_aposta), 'genre2': ['unknown'] * len(df_aposta)})
elif split_genres.shape[1] == 1:
    split_genres[1] = np.nan

# Agora sempre existem as colunas 0 e 1
df_aposta['genre1'] = split_genres[0].str.strip().fillna('unknown') if 0 in split_genres else 'unknown'
df_aposta['genre2'] = split_genres[1].str.strip().fillna('unknown') if 1 in split_genres else 'unknown'

print(df_aposta[['genres_first2', 'genre1', 'genre2']].head())

categorical_features = [
    'MPA', 'Languages', 'directors', 'writers', 'stars', 'genre1', 'genre2',
    'oscar_nominated', 'globe_nominated', 'globe_winner'
]
text_features = ['description']

# 4. Imputar valores ausentes
df_aposta['description'] = df_aposta['description'].fillna('')
for col in categorical_features:
    if col in df_aposta.columns:
        df_aposta[col] = df_aposta[col].fillna('unknown')

# 5. Pipeline de pré-processamento igual ao do treino
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])
text_transformer = Pipeline(steps=[
    ('tfidf', TfidfVectorizer(max_features=2000, stop_words='english'))
])

# 6. Carregar o modelo XGBoost treinado e o pré-processador treinado
best_xgb = joblib.load("Joblib\best_xgboost.joblib")
# Carregar o pré-processador treinado
preprocessor = joblib.load("Joblib\preprocessor.joblib")

# 7. Pré-processar os dados de aposta (use .transform)
X_aposta = df_aposta[numeric_features + categorical_features + text_features]
X_aposta_proc = preprocessor.transform(X_aposta)

# 8. Gerar probabilidades de vitória
probas = best_xgb.predict_proba(X_aposta_proc)[:, 1]

# 9. Gerar DataFrame de apostas
df_aposta['prob_vencer_oscar'] = probas

# 10. Exibir/apostar: top 10 filmes com maior chance
top_apostas = df_aposta.sort_values('prob_vencer_oscar', ascending=False)
print("\nTop 10 apostas para vencedor do Oscar:")
print(top_apostas[['Title', 'Year', 'prob_vencer_oscar']].head(10))

# 11. Salvar apostas para análise posterior
top_apostas.to_csv("apostas_oscar_xgboost.csv", index=False)