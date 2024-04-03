import requests
import random 
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def extraire_premiere_valeur(texte_stat):
    matches = re.findall(r'\d+', texte_stat)
    return matches[0] if matches else None

base_url_template = "https://www.dofus.com/fr/mmorpg/encyclopedie/equipements?text=&EFFECTMAIN_and_or=AND&object_level_min=1&object_level_max=200&EFFECT_and_or=AND&display=table&page={}"
total_pages = 104
data = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

for page_num in range(1, total_pages + 1):
    print(f"Traitement de la page {page_num} sur {total_pages}")
    page_url = base_url_template.format(page_num)
    response = requests.get(page_url, headers=headers)

    if response.status_code != 200:
        print(f"Erreur lors de l'accès à la page {page_num}: {response.status_code}")
        continue  
    time.sleep(random.randint(5, 10))  # Pause après chaque page principale

    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.find_all('tr')[1:]

    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 5:
            continue

        lien_element = cells[1].find('a')
        if not lien_element:
            continue

        lien = "https://www.dofus.com" + lien_element['href']
        nom = lien_element.text.strip()
        niveau = cells[4].text.strip()

        print(f"Traitement de l'objet : {nom}")

        response_detail = requests.get(lien, headers=headers)
        if response_detail.status_code != 200:
            print(f"Erreur lors de l'accès à la page de détail pour {nom}: {response_detail.status_code}")
            continue
        numrandom = random.randint(5,10)
        time.sleep(numrandom)  # Pause après chaque requête de détail
        print(numrandom)

        soup_detail = BeautifulSoup(response_detail.content, 'html.parser')
        statistiques = []
        stats_divs = soup_detail.find_all("div", class_="ak-title")

        if not stats_divs:
            print(f"Aucune statistique trouvée pour {nom}")
            continue

        for stat_div in stats_divs:
            stat_texte = stat_div.text.strip()
            premiere_valeur = extraire_premiere_valeur(stat_texte)
            if premiere_valeur:
                stat_nom = stat_texte.replace(premiere_valeur, '').strip()
                statistiques.append(f"{stat_nom}: {premiere_valeur}")

        data.append({
            "Nom": nom,
            "Niveau": niveau,
            "Statistiques": "; ".join(statistiques)
        })
    
df = pd.DataFrame(data)
output_file = "objets.xlsx"
df.to_excel(output_file, index=False)
print(f"Le fichier Excel a été sauvegardé sous : {output_file}")
