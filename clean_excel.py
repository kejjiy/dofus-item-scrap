import pandas as pd
import re

fichier_excel = 'objets.xlsx'  
df = pd.read_excel(fichier_excel)

def nettoyer_texte(texte):
    # Supprimer "à" et tout ce qui suit jusqu'à une lettre, puis continuer jusqu'à ";"
    texte = re.sub(r'à[^a-zA-Z]*([a-zA-Z])', r'\1', texte)
    # Supprimer "{~ps}" et "{~zs}"
    texte = texte.replace('{~ps}', '').replace('{~zs}', '')
    return texte

df.iloc[:, 2] = df.iloc[:, 2].astype(str).apply(nettoyer_texte)

df.to_excel('fichier_clean.xlsx', index=False)
