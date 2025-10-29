import pandas as pd
import numpy as np
from scipy.stats import spearmanr, pearsonr, shapiro, chi2_contingency, pointbiserialr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def eta_squared(x, y):
    """
    Calcula o coeficiente Eta (η) entre variável categórica x e contínua y.
    """
    grupos = [y[x == categoria] for categoria in np.unique(x)]
    ss_between = sum(len(g) * (g.mean() - y.mean())**2 for g in grupos)
    ss_total = sum((y - y.mean())**2)
    eta = np.sqrt(ss_between / ss_total)
    return eta


def get_correlation(df: pd.DataFrame, atributo: str, classe: str, tipo_atributo: str, tipo_classe: str, method: str):

    if df.empty:
        raise ValueError("O DataFrame está vazio.")
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Esperado um pandas.DataFrame, mas recebi {type(df)}")
    # 🔍 2️⃣ Verifica se as colunas existem
    if atributo not in df.columns:
        raise ValueError(f"A coluna '{atributo}' não existe no DataFrame.")
    if classe not in df.columns:
        raise ValueError(f"A coluna '{classe}' não existe no DataFrame.")

    x = df[atributo].dropna()
    y = df.loc[x.index, classe].dropna()
    
    resultado = {"atributo": atributo, "tipo": tipo_atributo, "classe": classe, "tipo": tipo_classe}

    if method == "Eta":
        resultado["method"] = "Eta"
        resultado["value"] = eta_squared(x, y)
    elif method == "Spearman":
        # Codifica ordinal como números se necessário
        x_num = pd.Categorical(x).codes
        corr, pval = spearmanr(x_num, y)
        resultado["method"] = "Spearman"
        resultado["value"] = corr
        resultado["p-value"] = pval
    elif method == "Pearson":
        corr, pval = pearsonr(x, y)
        resultado["method"] = "Pearson"
        resultado["value"] = corr
        resultado["p-value"] = pval
    elif method == "PointBiserial":
        r_pb, pval = pointbiserialr(x, y)
        resultado["method"] = "Point Biserial"
        resultado["value"] = r_pb
        resultado["p-value"] = pval      
    else:
        resultado["method"] = None
        resultado["value"] = None

    return resultado


def cramers_v(df: pd.DataFrame, attr1, attr2):
    """Calcula Cramer's V entre duas variáveis categóricas"""
    x = df[attr1]
    y = df[attr2]
    contingency_table = pd.crosstab(x, y)
    chi2, _, _, _ = chi2_contingency(contingency_table)
    n = contingency_table.sum().sum()
    k = min(contingency_table.shape)
    return np.sqrt(chi2 / (n * (k - 1)))


def shapiro_wilk(serie, attribute_name, significance):
    stat, p = shapiro(serie[attribute_name])

    interpretacao = (
        "Normal (não rejeita H0)" if p > float(significance)
        else "Não normal (rejeita H0)"
    )
    
    resultado = {
        "atributo": attribute_name,
        "method": "Shapiro-Wilk",
        "Estatística W": stat,
        "p-value": p,
        "Interpretação": interpretacao,
        "significance": significance
    }

    return resultado


def linear_regression(df: pd.DataFrame, features, target):
    # Selecionar features e target
    X = df[features]
    y = df[target]
    
    # Criar e treinar o modelo
    model = LinearRegression()
    model.fit(X, y)
    
    # Fazer previsões
    y_pred = model.predict(X)
    
    # Preparar resultados
    resultados = {
        'coeficientes': dict(zip(features, model.coef_)),
        'intercepto': model.intercept_,
        'mse': mean_squared_error(y, y_pred),
        'r2': r2_score(y, y_pred),
        'previsoes': y_pred
    }
    
    return model, resultados