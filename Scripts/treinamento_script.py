import pandas as pd
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

# Carregando o CSV com os filmes (o com as novas colunas)
df = pd.read_csv("filmes_imdb_com_premiacoes.csv")

# --- 1. Selecionar apenas os filmes que já têm resultado de premiação (se for treino supervisionado) ---
df = df[(df['oscar_winner'].notna()) & (df['oscar_nominated'].notna())]

# Definindo o alvo (y) — Exemplo: prever se o filme vence o Oscar
y = df['oscar_winner'].astype(int)  # ou 'globe_winner'

# --- 2. Remover colunas que não serão usadas diretamente como entrada ---
df = df.drop(columns=["Title", "Movie Link", "oscar_category", "globe_category", 
                      "oscar_nominated", "oscar_winner", "globe_nominated", "globe_winner"])

# --- 3. Definir colunas por tipo ---
numeric_features = ['Year', 'Duration', 'Rating', 'Votes', 'méta_score']
categorical_features = ['MPA', 'Languages']
text_features = ['description']

# --- 4. Pré-processadores ---
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

text_transformer = Pipeline(steps=[
    ('tfidf', TfidfVectorizer(max_features=100))])  # reduz a dimensionalidade

# --- 5. Combinar todos os transformadores ---
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features),
        ('txt', text_transformer, 'description')])

# --- 6. Criar pipeline final com modelo base ---
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# --- 7. Separar treino/teste ---
X = df[numeric_features + categorical_features + text_features]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 8. Treinar modelo ---
model.fit(X_train, y_train)

# --- 9. Avaliar ---
score = model.score(X_test, y_test)
print(f"Acurácia: {score:.2%}")
