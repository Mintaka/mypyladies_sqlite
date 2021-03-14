import os
import sys
import requests
import zipfile
import pathlib
import csv
import sqlite3

import data_sources

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


def create_missing_folders(folders):
    """Check and create folder if not exist"""
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)


def setup_db_connection(database_path=DATABASE_FOLDER + DATABASE_FILE):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    return connection, cursor


def create_data_structure(cursor):
    """Create tables for meteo data"""

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meteostations (
            id INTEGER PRIMARY KEY,
            name text,
            longtitude real,
            latitutde real
        );""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperatures (
            id INTEGER PRIMARY KEY,
            date text,
            temperature real
        );""")


def extract_data_file(filename, input_folder, output_folder):
    # Extract
    with zipfile.ZipFile(input_folder + '/' + filename,
                         'r') as zip_ref:
        zip_ref.extractall(output_folder)


def download_data_file(filename, region, download_folder, url_prefix):
    print(f"Proces data for region: {region} file: {filename}")
    # Download one data source
    url = f"{url_prefix}/{region}/{filename}"
    r = requests.get(url, allow_redirects=True)
    open(download_folder + '/' + filename, 'wb').write(r.content)


def get_meteostation_metadata(filename):
    """ Get last record from metadata and return (name, longtitude, latitude)"""
    with open(filename, encoding='cp1250') as _file:
        in_metadata = False
        metadata = []
        for line in _file.readlines():
            print("&", line.strip())
            line = line.strip()
            if line == "METADATA":
                in_metadata = True
            if in_metadata and line == "":
                break
            if in_metadata:
                metadata.append(line)
    print(metadata)
    splited_line = metadata[-1].split(";")
    return splited_line[1], splited_line[-3].replace(",", "."), splited_line[-2].replace(",", ".")


def update_measurement_format(measurement):
    try:
        updated_measurement = float(measurement.replace(",", "."))
    except ValueError:
        updated_measurement = measurement
    return updated_measurement


def insert_csv2db(csv_file, cursor, region=None):
    print(f"Read file: {csv_file}")
    meteostation_name, longtitude, latitude = get_meteostation_metadata(
        csv_file)
    cursor.execute(
            f'INSERT INTO meteostations VALUES (null, "{meteostation_name}", "{longtitude}", "{latitude}")')
    with open(csv_file, encoding='cp1250') as csv_data:
        csvreader = csv.reader(csv_data, delimiter=';')
        start_data_read = False
        for row in csvreader:
            # print(row)
            if ";".join(row).startswith("Rok;Měsíc;Den;Hodnota;Příznak"):
                start_data_read = True
                continue
            if not start_data_read:
                continue
            if len(row) < 4:
                print("Bad row: ", repr(row))
                continue
            # date format: YYYY-MM-DD
            date = f"{row[0]}-{row[1]}-{row[2].zfill(2)}"
            cursor.execute(f"""INSERT INTO temperatures VALUES 
                                 (null, "{date}", "{update_measurement_format(row[3])}")
                            """)


def fill_database(connection, cursor):
    create_data_structure(cursor)

    for region, files in data_sources.source_files.items():
        for filename in files:

            zipfilepath = DOWNLOAD_FOLDER + '/' + filename
            if not os.path.exists(zipfilepath):
                download_data_file(filename, region, DOWNLOAD_FOLDER,
                                   data_sources.average_temperature_prefix)

            csvfilepath = DATASETS_FOLDER + '/' + filename[:-4]
            if not os.path.exists(csvfilepath):
                extract_data_file(filename, DOWNLOAD_FOLDER, DATASETS_FOLDER)

            insert_csv2db(csvfilepath, cursor, region=region)

    connection.commit()

# data = cursor.execute(f'SELECT * FROM temperatures LIMIT 100;')
# print(data.fetchall())
# data = cursor.execute(f'SELECT count(*) FROM temperatures;')
# print(data.fetchall())
#
# data = cursor.execute(f'SELECT * FROM meteostations;')
# for _id, meteostation_name, longtitude, latitude in data.fetchall():
#     print([longtitude, latitude])


def main(args):
    if args is None:
        arg = sys.argv

    create_missing_folders(WORKING_FOLDERS)
    connection, cursor = setup_db_connection()
    fill_database(connection, cursor)


if __name__ == '__main__':
    main(None)
