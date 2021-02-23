import requests

url = "https://www.chmi.cz/files/portal/docs/meteo/ok/denni_data/T-AVG/Plzensky/L1PLMI01_T_N.csv.zip"
r = requests.get(url, allow_redirects=True)
open("L1PLMI01_T_N.csv.zip", "wb").write(r.content)



