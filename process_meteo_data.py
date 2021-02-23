import requests
import zipfile

url = "https://www.chmi.cz/files/portal/docs/meteo/ok/denni_data/T-AVG/Plzensky/L1PLMI01_T_N.csv.zip"
# TODO ziskat nazev souboru pomoci pathlib
filename = url.split("/")[-1]

r = requests.get(url, allow_redirects=True)
open(filename, "wb").write(r.content)

with zipfile.ZipFile(filename, "r") as zip_ref:
    zip_ref.extractall(".")


