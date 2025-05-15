import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from xgboost import XGBClassifier
import joblib

# 1. Carregar o dataset de apostas
df = pd.read_csv("IMDBest.IMDBest.com_generos.csv")

# 2. Filtrar apenas filmes SEM resultado de premiação
df_aposta = df[(df['oscar_winner'].isna()) & (df['oscar_nominated'].isna())].copy()

if df_aposta.empty:
    print("Nenhum filme novo encontrado para aposta (todos já possuem resultado de premiação).")
    exit()

# 3. Definir colunas por tipo
numeric_features = ['Year', 'Duration', 'Rating', 'Votes']

if 'genres_first2' not in df_aposta.columns:
    raise ValueError("A coluna 'genres_first2' não existe no arquivo CSV.")

df_aposta['genres_first2'] = df_aposta['genres_first2'].fillna('')

split_genres = df_aposta['genres_first2'].str.split(',', n=1, expand=True)
if split_genres.shape[1] == 0:
    split_genres = pd.DataFrame({'genre1': ['unknown'] * len(df_aposta), 'genre2': ['unknown'] * len(df_aposta)})
elif split_genres.shape[1] == 1:
    split_genres[1] = np.nan

df_aposta['genre1'] = split_genres[0].str.strip().fillna('unknown') if 0 in split_genres else 'unknown'
df_aposta['genre2'] = split_genres[1].str.strip().fillna('unknown') if 1 in split_genres else 'unknown'

categorical_features = [
    'MPA', 'Languages', 'directors', 'writers', 'stars', 'genre1', 'genre2',
    'oscar_nominated', 'globe_nominated', 'globe_winner'
]
text_features = ['description']

df_aposta['description'] = df_aposta['description'].fillna('')
for col in categorical_features:
    if col in df_aposta.columns:
        df_aposta[col] = df_aposta[col].fillna('unknown')

# 4. Carregar os modelos treinados e seus preprocessors
xgb_oscar_nominated = joblib.load("Joblib/best_oscar_nominated_xgboost.joblib")
preproc_oscar_nominated = joblib.load("Joblib/preprocessor_oscar_nominated.joblib")

xgb_oscar_winner = joblib.load("Joblib/best_oscar_winner_xgboost.joblib")
preproc_oscar_winner = joblib.load("Joblib/preprocessor_oscar_winner.joblib")

xgb_globe_nominated = joblib.load("Joblib/best_globe_nominated_xgboost.joblib")
preproc_globe_nominated = joblib.load("Joblib/preprocessor_globe_nominated.joblib")

xgb_globe_winner = joblib.load("Joblib/best_globe_winner_xgboost.joblib")
preproc_globe_winner = joblib.load("Joblib/preprocessor_globe_winner.joblib")

# 5. Definir features para cada alvo (sem a coluna-alvo)
cat_oscar_nominated = [c for c in categorical_features if c != 'oscar_nominated']
cat_oscar_winner = [c for c in categorical_features if c != 'oscar_winner']
cat_globe_nominated = [c for c in categorical_features if c != 'globe_nominated']
cat_globe_winner = [c for c in categorical_features if c != 'globe_winner']

features_oscar_nominated = numeric_features + cat_oscar_nominated + text_features
features_oscar_winner = numeric_features + cat_oscar_winner + text_features
features_globe_nominated = numeric_features + cat_globe_nominated + text_features
features_globe_winner = numeric_features + cat_globe_winner + text_features

# 6. Pré-processar e prever para cada alvo
X_oscar_nominated = df_aposta[features_oscar_nominated]
X_oscar_winner = df_aposta[features_oscar_winner]
X_globe_nominated = df_aposta[features_globe_nominated]
X_globe_winner = df_aposta[features_globe_winner]

df_aposta['prob_indicado_oscar'] = xgb_oscar_nominated.predict_proba(preproc_oscar_nominated.transform(X_oscar_nominated))[:, 1]
df_aposta['prob_vencedor_oscar'] = xgb_oscar_winner.predict_proba(preproc_oscar_winner.transform(X_oscar_winner))[:, 1]
df_aposta['prob_indicado_globo'] = xgb_globe_nominated.predict_proba(preproc_globe_nominated.transform(X_globe_nominated))[:, 1]
df_aposta['prob_vencedor_globo'] = xgb_globe_winner.predict_proba(preproc_globe_winner.transform(X_globe_winner))[:, 1]

# 7. Exibir/apostar: top 10 para cada alvo
print("\nTop 10 apostas para indicação ao Oscar:")
print(df_aposta.sort_values('prob_indicado_oscar', ascending=False)[['Title', 'Year', 'prob_indicado_oscar']].head(10))

print("\nTop 10 apostas para vencedor do Oscar:")
print(df_aposta.sort_values('prob_vencedor_oscar', ascending=False)[['Title', 'Year', 'prob_vencedor_oscar']].head(10))

print("\nTop 10 apostas para indicação ao Globo de Ouro:")
print(df_aposta.sort_values('prob_indicado_globo', ascending=False)[['Title', 'Year', 'prob_indicado_globo']].head(10))

print("\nTop 10 apostas para vencedor do Globo de Ouro:")
print(df_aposta.sort_values('prob_vencedor_globo', ascending=False)[['Title', 'Year', 'prob_vencedor_globo']].head(10))

# 8. Salvar apostas para análise posterior
df_aposta.to_csv("apostas_multialvos_xgboost.csv", index=False)