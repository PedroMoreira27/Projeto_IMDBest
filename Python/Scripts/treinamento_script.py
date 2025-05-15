import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from sklearn.metrics import f1_score, precision_recall_curve, classification_report, confusion_matrix
import joblib

# 1. Carregar o novo dataset
df = pd.read_csv("IMDBest.IMDBest.com_generos.csv")

# 2. Selecionar apenas os filmes que já têm resultado de premiação (supervisionado)
df = df[
    (df['oscar_winner'].notna()) &
    (df['oscar_nominated'].notna()) &
    (df['globe_nominated'].notna()) &
    (df['globe_winner'].notna())
]

# 3. Definir colunas por tipo
numeric_features = ['Year', 'Duration', 'Rating', 'Votes']
df[['genre1', 'genre2']] = df['genres_first2'].str.split(',', n=1, expand=True)
categorical_features = [
    'MPA', 'Languages', 'directors', 'writers', 'stars', 'genre1', 'genre2',
    'oscar_nominated', 'globe_nominated', 'globe_winner'
]
text_features = ['description']

# Imputar valores ausentes
df['description'] = df['description'].fillna('')
for col in categorical_features:
    df[col] = df[col].fillna('unknown')

# 4. Pré-processadores
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

# 5. Combinar todos os transformadores
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features),
        ('txt', text_transformer, 'description')
    ]
)

# 6. Salvar o preprocessor após o fit
X = df[numeric_features + categorical_features + text_features]
preprocessor.fit(X)
joblib.dump(preprocessor, "preprocessor.joblib")

# 7. Alvos e nomes dos modelos
alvos = {
    "oscar_nominated": "best_oscar_nominated_xgboost.joblib",
    "oscar_winner": "best_oscar_winner_xgboost.joblib",
    "globe_nominated": "best_globe_nominated_xgboost.joblib",
    "globe_winner": "best_globe_winner_xgboost.joblib"
}

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [3, 6],
    'scale_pos_weight': [5, 10]
}

for alvo, nome_arquivo in alvos.items():
    print(f"\n=== Treinando modelo para: {alvo} ===")
    # Remova o alvo das features para não vazar informação!
    cat_features = [c for c in categorical_features if c != alvo]
    features = numeric_features + cat_features + text_features
    X = df[features]
    y = df[alvo].astype(int)

    # Crie o preprocessor específico para este alvo
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, cat_features),
            ('txt', text_transformer, 'description')
        ]
    )
    preprocessor.fit(X)
    joblib.dump(preprocessor, f"preprocessor_{alvo}.joblib")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    X_train_proc = preprocessor.transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    smote = SMOTE(random_state=42)
    X_train_bal, y_train_bal = smote.fit_resample(X_train_proc, y_train)

    xgb = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
    grid = GridSearchCV(xgb, param_grid, scoring='f1', cv=3, n_jobs=-1)
    grid.fit(X_train_bal, y_train_bal)
    print(f"Melhores parâmetros: {grid.best_params_}")

    best_model = grid.best_estimator_
    joblib.dump(best_model, nome_arquivo)

    y_scores = best_model.predict_proba(X_test_proc)[:, 1]
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_scores)
    f1s = 2 * (precisions * recalls) / (precisions + recalls + 1e-8)
    best_idx = np.argmax(f1s)
    best_threshold = thresholds[best_idx]
    best_f1 = f1s[best_idx]
    print(f"Melhor threshold para f1-score: {best_threshold:.3f} (f1-score={best_f1:.3f})")
    y_pred_best = (y_scores > best_threshold).astype(int)
    print("Matriz de confusão (threshold ótimo):")
    print(confusion_matrix(y_test, y_pred_best))
    print("Relatório de classificação (threshold ótimo):")
    print(classification_report(y_test, y_pred_best, zero_division=0))
