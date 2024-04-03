import subprocess
import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from openpyxl import Workbook

python_interpreter = "C:\\Users\\kingd\\myenv\\Scripts\\python.exe"

scripts = ["scrape_dofus.py", "clean_excel.py", "feuilletage.py"]

for script in scripts:
    try:
        subprocess.run([python_interpreter, script], check=True)
        print(f"{script} a été exécuté avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Le script {script} a échoué avec l'erreur suivante : {e}")
        break  

