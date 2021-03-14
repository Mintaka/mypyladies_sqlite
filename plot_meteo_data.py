from pathlib import Path
import sqlite3

from matplotlib import pyplot as plt

from process_meteo_data import setup_db_connection, EXPORTS_FOLDER

connection, cursor = setup_db_connection()

data = cursor.execute(f'SELECT * FROM temperatures LIMIT 100;').fetchall()

_, date, temp = list(zip(*data))

plt.plot(temp)

plt.savefig(EXPORTS_FOLDER + '/' + "temp.png")

plt.show()
