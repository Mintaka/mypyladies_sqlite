import os
import requests
import zipfile
import pathlib
import csv
import sqlite3

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

def update_measurement_format(measurement):
    try:
        updated_measurement = float(measurement.replace(",", "."))
    except ValueError:
        updated_measurement = measurement
    return updated_measurement


# Read from CSV and insert into database
csv_files = (list(pathlib.Path(DATASETS_FOLDER).glob('*.csv')))
for csv_file in csv_files:
    print(f"Read file: {csv_file}")
    with open(csv_file, encoding='cp1250') as csv_data:
        csvreader = csv.reader(csv_data, delimiter=';')
        for row in csvreader:
            print(row)
            if len(row) < 4:
                continue
            cursor.execute(f'INSERT INTO temperatures VALUES (null, "{row[0]}", "{row[1]}", "{row[2]}", "{update_measurement_format(row[3])}")')

connection.commit()

data = cursor.execute(f'SELECT * FROM temperatures;')
print(data.fetchall())
data = cursor.execute(f'SELECT count(*) FROM temperatures;')
print(data.fetchall())

