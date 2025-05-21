import os
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
import joblib

# Base do diretório do script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carregar dados base (para features dos filmes)
df = pd.read_csv(os.path.join(BASE_DIR, "IMDBest.IMDBest.com_generos.csv"), low_memory=False)

# Carregar modelos e preprocessadores
MODELOS = {
    "oscar_nominated": (
        joblib.load(os.path.join(BASE_DIR, "../Joblib/best_oscar_nominated_xgboost.joblib")),
        joblib.load(os.path.join(BASE_DIR, "../Joblib/preprocessor_oscar_nominated.joblib")),
        ['Year', 'Duration', 'Rating', 'Votes', 'MPA', 'Languages', 'directors', 'writers', 'stars', 'genre1', 'genre2', 'globe_nominated', 'globe_winner', 'description']
    ),
    "oscar_winner": (
        joblib.load(os.path.join(BASE_DIR, "../Joblib/best_oscar_winner_xgboost.joblib")),
        joblib.load(os.path.join(BASE_DIR, "../Joblib/preprocessor_oscar_winner.joblib")),
        ['Year', 'Duration', 'Rating', 'Votes', 'MPA', 'Languages', 'directors', 'writers', 'stars', 'genre1', 'genre2', 'oscar_nominated', 'globe_nominated', 'globe_winner', 'description']
    ),
    "globe_nominated": (
        joblib.load(os.path.join(BASE_DIR, "../Joblib/best_globe_nominated_xgboost.joblib")),
        joblib.load(os.path.join(BASE_DIR, "../Joblib/preprocessor_globe_nominated.joblib")),
        ['Year', 'Duration', 'Rating', 'Votes', 'MPA', 'Languages', 'directors', 'writers', 'stars', 'genre1', 'genre2', 'oscar_nominated', 'globe_winner', 'description']
    ),
    "globe_winner": (
        joblib.load(os.path.join(BASE_DIR, "../Joblib/best_globe_winner_xgboost.joblib")),
        joblib.load(os.path.join(BASE_DIR, "../Joblib/preprocessor_globe_winner.joblib")),
        ['Year', 'Duration', 'Rating', 'Votes', 'MPA', 'Languages', 'directors', 'writers', 'stars', 'genre1', 'genre2', 'oscar_nominated', 'globe_nominated', 'description']
    ),
}

app = FastAPI()

class ConsultaRequest(BaseModel):
    title: str
    year: int
    categorias: List[str]

def preparar_features(filme, features):
    # Extrair generos se não existirem
    if 'genres_first2' in filme and (('genre1' not in filme) or ('genre2' not in filme)):
        genres = filme['genres_first2'].split(',')
        filme['genre1'] = genres[0].strip() if len(genres) > 0 else 'unknown'
        filme['genre2'] = genres[1].strip() if len(genres) > 1 else 'unknown'

    # Garantir que todas as features existam
    for col in features:
        if col not in filme or pd.isna(filme[col]):
            filme[col] = 0 if col in ['Year', 'Duration', 'Rating', 'Votes'] else 'unknown'

    return pd.DataFrame([filme])[features]

@app.post("/predict")
def predict(request: ConsultaRequest):
    filme = df[(df['Title'].str.lower() == request.title.lower()) & (df['Year'] == request.year)]

    if filme.empty:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    filme = filme.iloc[0].to_dict()

    if not pd.isna(filme.get('oscar_nominated')) or not pd.isna(filme.get('oscar_winner')):
        raise HTTPException(status_code=400, detail="Filme já possui indicação ou premiação")

    predictions = {}

    for cat in request.categorias:
        if cat not in MODELOS:
            predictions[cat] = None
            continue
        model, preproc, features = MODELOS[cat]
        X = preparar_features(filme.copy(), features)
        prob = float(model.predict_proba(preproc.transform(X))[:, 1])
        predictions[cat] = prob

    return {
        "title": request.title,
        "year": request.year,
        "predictions": predictions
    }

@app.get("/top10")
def top10(categoria: str = Query(..., enum=list(MODELOS.keys()))):
    model, preproc, features = MODELOS[categoria]

    # Filtrar filmes sem premiações
    df_filmes = df[(df['oscar_winner'].isna()) & (df['oscar_nominated'].isna())].copy()

    # Preencher genre1 e genre2
    split_genres = df_filmes['genres_first2'].str.split(',', n=1, expand=True)
    df_filmes['genre1'] = split_genres[0].str.strip().fillna('unknown')
    if split_genres.shape[1] > 1:
        df_filmes['genre2'] = split_genres[1].str.strip().fillna('unknown')
    else:
        df_filmes['genre2'] = 'unknown'

    # Garantir que todas as colunas existam
    for col in features:
        if col not in df_filmes.columns:
            df_filmes[col] = 'unknown'
        df_filmes[col] = df_filmes[col].fillna('unknown' if col not in ['Year', 'Duration', 'Rating', 'Votes'] else 0)

    X = df_filmes[features]
    probs = model.predict_proba(preproc.transform(X))[:, 1]
    df_filmes['prob'] = probs

    top = df_filmes.sort_values('prob', ascending=False).head(10)
    return top[['Title', 'Year', 'prob']].to_dict(orient='records')
