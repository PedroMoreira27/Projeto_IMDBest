import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_predict, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, precision_recall_curve
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
import joblib

# 1. Carregar o novo dataset
df = pd.read_csv("IMDBest.IMDBest.com_generos.csv")

# 2. Selecionar apenas os filmes que já têm resultado de premiação (supervisionado)
df = df[(df['oscar_winner'].notna()) & (df['oscar_nominated'].notna())]

# 3. Definir o alvo (y)
y = df['oscar_winner'].astype(int)

print("Distribuição das classes no dataset:")
print(y.value_counts())

# 4. Remover colunas que não serão usadas diretamente como entrada
df = df.drop(columns=[
    "Title", "Movie Link", "oscar_category", "globe_category",
    "oscar_winner"
], errors='ignore')

# 5. Definir colunas por tipo
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

# 6. Pré-processadores
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

# 7. Combinar todos os transformadores
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features),
        ('txt', text_transformer, 'description')
    ]
)

# 8. Separar treino/teste
X = df[numeric_features + categorical_features + text_features]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Após definir o preprocessor:
preprocessor.fit(X_train)  # ou preprocessor.fit_transform(X_train)

# Só depois do fit, salve:
joblib.dump(preprocessor, "preprocessor.joblib")

# 9. Pré-processar X_train para aplicar SMOTE
X_train_proc = preprocessor.transform(X_train)
X_test_proc = preprocessor.transform(X_test)

# 10. Aplicar SMOTE para balanceamento
smote = SMOTE(random_state=42)
X_train_bal, y_train_bal = smote.fit_resample(X_train_proc, y_train)

# 11. Treinar e avaliar modelos com dados balanceados
modelos = {
    "RandomForest": RandomForestClassifier(n_estimators=500, random_state=42, class_weight='balanced'),
    "LogisticRegression": LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42),
    "GradientBoosting": GradientBoostingClassifier(n_estimators=200, random_state=42),
    "XGBoost": XGBClassifier(n_estimators=200, random_state=42, scale_pos_weight=10, use_label_encoder=False, eval_metric='logloss')
}

param_grids = {
    "RandomForest": {
        'n_estimators': [200, 500],
        'max_depth': [None, 10],
        'min_samples_split': [2, 5]
    },
    "LogisticRegression": {
        'C': [0.1, 1, 10]
    },
    "GradientBoosting": {
        'n_estimators': [100, 200],
        'max_depth': [3, 6]
    },
    "XGBoost": {
        'n_estimators': [100, 200],
        'max_depth': [3, 6],
        'scale_pos_weight': [5, 10]
    }
}

best_models = {}

for nome, clf in modelos.items():
    print(f"\n=== {nome} (GridSearchCV) ===")
    grid = GridSearchCV(clf, param_grids[nome], scoring='f1', cv=3, n_jobs=-1)
    grid.fit(X_train_bal, y_train_bal)
    print(f"Melhores parâmetros: {grid.best_params_}")
    best_models[nome] = grid.best_estimator_

    # Salva o modelo treinado com joblib
    joblib.dump(best_models[nome], f"best_{nome.lower()}_model.joblib")

    # Avaliação no teste
    y_scores = best_models[nome].predict_proba(X_test_proc)[:, 1]
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
