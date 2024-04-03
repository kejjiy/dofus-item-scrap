import pandas as pd
import re
from openpyxl import Workbook

fichier_excel = 'fichier_clean.xlsx'
df = pd.read_excel(fichier_excel)

nouveau_classeur = Workbook()
del nouveau_classeur['Sheet']  

for _, row in df.iterrows():
    nom_objet = row['Nom']
    niveau_objet = row['Niveau']
    statistiques = row['Statistiques']

    statistiques = str(row['Statistiques'])  
    statistiques = re.sub(r'à[^a-zA-Z]*([a-zA-Z])', r'\1', statistiques)
    statistiques = statistiques.replace('{~ps}', '').replace('{~zs}', '')

    feuille = nouveau_classeur.create_sheet(title=nom_objet)
    feuille.append(['Niveau de l\'objet', niveau_objet])

    # Ajouter les statistiques
    for stat in statistiques.split(';'):
        stat = stat.strip()  # Enlever les espaces blancs avant et après la chaîne
        if stat:
            # Diviser la chaîne sans espace avant les deux-points
            if ':' in stat:
                parts = stat.split(':')
                if len(parts) == 2:
                    nom_stat, valeur = parts
                    feuille.append([nom_stat.strip(), valeur.strip()])
                else:
                    print(f"Impossible de diviser correctement la chaîne '{stat}'")
            else:
                print(f"La chaîne '{stat}' ne contient pas ':' et a été ignorée.")

nouveau_classeur.save('feuilltes.xlsx')
