import requests
import zipfile
import pathlib
import csv
import sqlite3

DATABASE_FILE = './.database/mojedata.sqlite'
DOWNLOAD_FOLDER = './.download'
DATASETS_FOLDER = './.datasets'

connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS temperatures (
        id INTEGER PRIMARY KEY,
        year int,
        month int,
        day int,
        temperatue real
    );""")

url = 'https://www.chmi.cz/files/portal/docs/meteo/ok/denni_data/T-AVG/Plzensky/L1PLMI01_T_N.csv.zip'
filename = url.split('/')[-1]

r = requests.get(url, allow_redirects=True)
open(DOWNLOAD_FOLDER + '/' + filename, 'wb').write(r.content)

with zipfile.ZipFile(DOWNLOAD_FOLDER + '/' + filename, 'r') as zip_ref:
    zip_ref.extractall(DATASETS_FOLDER)

csv_files = (list(pathlib.Path(DATASETS_FOLDER).glob('*.csv')))
for csv_file in csv_files:
    print(csv_file)
    with open(csv_file, encoding='cp1250') as csv_data:
        csvreader = csv.reader(csv_data, delimiter=';')
        for row in csvreader:
            print(row)
            if len(row) < 4:
                continue
            cursor.execute(f'INSERT INTO temperatures VALUES (null, "{row[0]}", "{row[1]}", "{row[2]}", "{row[3]}")')

connection.commit()

data = cursor.execute(f'SELECT count(*) FROM temperatures;')
print(data.fetchall())
data = cursor.execute(f'SELECT * FROM temperatures;')
print(data.fetchall())

