import pandas as pd
import numpy as np
from scipy.stats import spearmanr, pearsonr


def eta_squared(x, y):
    """
    Calcula o coeficiente Eta (η) entre variável categórica x e contínua y.
    """
    grupos = [y[x == categoria] for categoria in np.unique(x)]
    ss_between = sum(len(g) * (g.mean() - y.mean())**2 for g in grupos)
    ss_total = sum((y - y.mean())**2)
    eta = np.sqrt(ss_between / ss_total)
    return eta


def correlate_continuous(df: pd.DataFrame, atributo: str, classe: str, tipo_atributo: str, tipo_classe: str):
    x = df[atributo].dropna()
    y = df.loc[x.index, classe].dropna()
    
    resultado = {"atributo": atributo, "tipo": tipo_atributo, "classe": classe}

    if tipo_atributo == "nominal":
        resultado["método"] = "Eta (categórico × contínuo)"
        resultado["valor"] = eta_squared(x, y)
    elif tipo_atributo == "ordinal":
        # Codifica ordinal como números se necessário
        x_num = pd.Categorical(x).codes
        corr, pval = spearmanr(x_num, y)
        resultado["método"] = "Spearman"
        resultado["valor"] = corr
        resultado["p-valor"] = pval
    elif tipo_atributo == "contínua":
        corr, pval = pearsonr(x, y)
        resultado["método"] = "Pearson"
        resultado["valor"] = corr
        resultado["p-valor"] = pval
    else:
        resultado["método"] = None
        resultado["valor"] = None

    return resultado


# Exemplo de uso:
# df = pd.DataFrame({
#     "satisfacao": [1, 2, 3, 4, 5],
#     "renda": [2000, 2200, 2500, 3000, 3200]
#})

#resultado = spearman_corr(df, "satisfacao", "renda")
#print(f"Spearman rho = {resultado['rho']}, p-valor = {resultado['p-valor']}")

