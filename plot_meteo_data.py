from pathlib import Path
import sqlite3

from matplotlib import pyplot as plt
import numpy as np
# from matplotlib import pylab

DATABASE_FILE = "mydata.sqlite"
DATABASE_FOLDER = './.database/'
EXPORTS_FOLDER = './.exports/'

connection = sqlite3.connect(DATABASE_FOLDER + DATABASE_FILE)
cursor = connection.cursor()

data = cursor.execute(f'SELECT * FROM temperatures LIMIT 100;').fetchall()

_, date, temp = list(zip(*data))

plt.plot(temp)


plt.show()
