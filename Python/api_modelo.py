import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import joblib

# Carregar dados base (para features dos filmes)
df = pd.read_csv("IMDBest.IMDBest.com_generos.csv", low_memory=False)

# Carregar modelos e preprocessors
MODELOS = {
    "oscar_nominated": (
        joblib.load("Joblib/best_oscar_nominated_xgboost.joblib"),
        joblib.load("Joblib/preprocessor_oscar_nominated.joblib"),
        ['Year', 'Duration', 'Rating', 'Votes', 'MPA', 'Languages', 'directors', 'writers', 'stars', 'genre1', 'genre2', 'globe_nominated', 'globe_winner', 'description']
    ),
    "oscar_winner": (
        joblib.load("Joblib/best_oscar_winner_xgboost.joblib"),
        joblib.load("Joblib/preprocessor_oscar_winner.joblib"),
        ['Year', 'Duration', 'Rating', 'Votes', 'MPA', 'Languages', 'directors', 'writers', 'stars', 'genre1', 'genre2', 'oscar_nominated', 'globe_nominated', 'globe_winner', 'description']
    ),
    "globe_nominated": (
        joblib.load("Joblib/best_globe_nominated_xgboost.joblib"),
        joblib.load("Joblib/preprocessor_globe_nominated.joblib"),
        ['Year', 'Duration', 'Rating', 'Votes', 'MPA', 'Languages', 'directors', 'writers', 'stars', 'genre1', 'genre2', 'oscar_nominated', 'globe_winner', 'description']
    ),
    "globe_winner": (
        joblib.load("Joblib/best_globe_winner_xgboost.joblib"),
        joblib.load("Joblib/preprocessor_globe_winner.joblib"),
        ['Year', 'Duration', 'Rating', 'Votes', 'MPA', 'Languages', 'directors', 'writers', 'stars', 'genre1', 'genre2', 'oscar_nominated', 'globe_nominated', 'description']
    ),
}

# FastAPI app
app = FastAPI()

class ConsultaRequest(BaseModel):
    title: str
    year: int
    categorias: list

def preparar_features(filme, features):
    # Prepara as features do filme para predição
    row = filme.copy()
    # Garantir colunas auxiliares
    if 'genres_first2' in row and (('genre1' not in row) or ('genre2' not in row)):
        genres = row['genres_first2'].split(',')
        row['genre1'] = genres[0].strip() if len(genres) > 0 else 'unknown'
        row['genre2'] = genres[1].strip() if len(genres) > 1 else 'unknown'
    for col in features:
        if col not in row or pd.isna(row[col]):
            row[col] = 'unknown' if col not in ['Year', 'Duration', 'Rating', 'Votes'] else 0
    return pd.DataFrame([row])[features]

@app.post("/predict")
def predict(request: ConsultaRequest):
    # Buscar filme pelo título e ano
    filme = df[(df['Title'].str.lower() == request.title.lower()) & (df['Year'] == request.year)]
    if filme.empty:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    filme = filme.iloc[0].to_dict()
    # Se já tem premiação, não retorna probabilidade
    if not pd.isna(filme.get('oscar_nominated')) or not pd.isna(filme.get('oscar_winner')):
        raise HTTPException(status_code=400, detail="Filme já possui indicação ou premiação")
    result = {}
    for cat in request.categorias:
        if cat not in MODELOS:
            result[cat] = None
            continue
        model, preproc, features = MODELOS[cat]
        X = preparar_features(filme, features)
        prob = float(model.predict_proba(preproc.transform(X))[:, 1])
        result[cat] = prob
    return result

@app.get("/top10")
def top10(categoria: str = Query(..., enum=list(MODELOS.keys()))):
    model, preproc, features = MODELOS[categoria]
    # Filtrar apenas filmes sem premiação
    df_filmes = df[(df['oscar_winner'].isna()) & (df['oscar_nominated'].isna())].copy()
    # Preencher genres
    split_genres = df_filmes['genres_first2'].str.split(',', n=1, expand=True)
    df_filmes['genre1'] = split_genres[0].str.strip().fillna('unknown')
    df_filmes['genre2'] = split_genres[1].str.strip().fillna('unknown') if split_genres.shape[1] > 1 else 'unknown'
    for col in features:
        if col not in df_filmes.columns:
            df_filmes[col] = 'unknown'
        df_filmes[col] = df_filmes[col].fillna('unknown' if col not in ['Year', 'Duration', 'Rating', 'Votes'] else 0)
    X = df_filmes[features]
    probs = model.predict_proba(preproc.transform(X))[:, 1]
    df_filmes['prob'] = probs
    top = df_filmes.sort_values('prob', ascending=False).head(10)
    return top[['Title', 'Year', 'prob']].to_dict(orient='records')