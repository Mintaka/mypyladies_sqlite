import os
import requests
import zipfile
import pathlib
import csv
import sqlite3
import pandas as pd

import data_sources

def create_missing_folders(folders):
    """Check and create folder if not exist"""
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def create_data_structure(cursor):
    """Create tables for meteo data"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperatures (
            id INTEGER PRIMARY KEY,
            year int,
            month int,
            day int,
            temperatue real
        );""")


DATABASE_FILE = "mydata.sqlite"

DATABASE_FOLDER = './.database/'
DOWNLOAD_FOLDER = './.download/'
DATASETS_FOLDER = './.datasets/'
EXPORTS_FOLDER = './.exports/'

WORKING_FOLDERS = [
                    DATABASE_FOLDER,
                    DOWNLOAD_FOLDER,
                    DATASETS_FOLDER,
                    EXPORTS_FOLDER,
                  ]

df_all =  pd.DataFrame(columns = ["stanice","datum","Hodnota","Příznak"])

create_missing_folders(WORKING_FOLDERS)
connection = sqlite3.connect(DATABASE_FOLDER + DATABASE_FILE)
cursor = connection.cursor()
create_data_structure(cursor)


url_prefix = data_sources.average_temperature_prefix
# Read and extract all data sources
for region, files in data_sources.source_files.items():
    for filename in files:
        print(f"Proces data for region: {region} file: {filename}")

        # Download one data source
        url = f"{url_prefix}/{region}/{filename}"
        filename = pathlib.Path(url).name
        r = requests.get(url, allow_redirects=True)
        open(DOWNLOAD_FOLDER + '/' + filename, 'wb').write(r.content)

        # Extract
        with zipfile.ZipFile(DOWNLOAD_FOLDER + '/' + filename, 'r') as zip_ref:
            zip_ref.extractall(DATASETS_FOLDER)

# Read from CSV and insert into database
csv_files = (list(pathlib.Path(DATASETS_FOLDER).glob('*.csv')))
for csv_file in csv_files:
    #read the csv file, determine where the data begin
    with open (csv_file, encoding='cp1250') as csv_data:
        obsah = csv_data.read()
        pozice = obsah.index("Rok;Měsíc;Den;Hodnota;Příznak") + 29
        print(pozice)
        obsah = obsah[pozice:]
    #create a file with data only for import
    with open ('data_pro_zapis.csv', mode = 'w', encoding = "cp1250") as soubor:
        print(obsah, file = soubor)
    #create a pd Dataframe from the individual file, append pd Dataframe with all the data
    sloupce = ["Rok","Měsíc","Den","Hodnota","Příznak"]
    df_from_file = pd.read_csv("data_pro_zapis.csv", delimiter = ";", names = sloupce, parse_dates = [[0,1,2]],decimal = ',')
    df_from_file['stanice'] = pathlib.Path(csv_file).stem
    df_from_file["datum"] = df_from_file["Rok_Měsíc_Den"].dt.strftime("%d/%m/%Y") 
    df_from_file = df_from_file[["stanice","datum","Hodnota","Příznak"]]
    df_all =  df_all.append(df_from_file)
    
print(df_all)
#insert all data to sql db
df_all.to_sql("temperatures", connection, if_exists = "replace")
  
data = cursor.execute(f'SELECT count(*) FROM temperatures;')
print(data.fetchall())

