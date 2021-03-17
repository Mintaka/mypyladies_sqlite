#!python
# -*- coding: utf-8 -*-

__author__ = "Tomas Zitka"
__email__ = "tozitka@gmail.com"
import numpy as np
from matplotlib import pyplot as plt

from process_meteo_data import setup_db_connection, EXPORTS_FOLDER



def plot_temp_by_meteostation(cursor, meteostation_id,
                              start: int = 1970,
                              end: int = 1980):
    """
    Plots temperature measured at station with meteostastion_id
    as time series for each year, colors years in ascending colors.
    Saves the plot into EXPORTS_FOLDER + '/' + f"temp_{name}_meteostation.png"

    :param cursor: cursor to database
    """

    name = cursor.execute(f'SELECT name FROM meteostations '
                          f'WHERE id == {meteostation_id};').fetchone()[0]

    # MAGIC
    colors = plt.cm.viridis(np.linspace(0, 1, end-start + 1))
    # END of MAGIC
    for ii, year in enumerate(range(start, end + 1)):
        data = cursor.execute(f'SELECT * FROM temperatures '
                              f'WHERE meteostation_id == {meteostation_id} '
                              f"and date LIKE '{year}%'").fetchall()
        if len(data) == 0:
            print(f"Data missing for {name} {year}")
            continue

        _, _meteostation_id, date, temp = list(zip(*data))

        plt.plot(temp, label=year, color=colors[ii])

    plt.legend()

    plt.savefig(EXPORTS_FOLDER + '/' + f"temp_{name}_meteostation.png")


def plot_temp_by_year(cursor, year=1989):
    """
    Plots data from given year for all available meteostations.
    Saves result into EXPORTS_FOLDER + '/' + f"temp_{year}_meteostations.png"
    """
    for meteostation_id in range(1, 26):
        data = cursor.execute(f'SELECT * FROM temperatures '
                              f'WHERE meteostation_id == {meteostation_id} '
                              f"and date LIKE '{year}%'").fetchall()

        name = cursor.execute(f'SELECT name FROM meteostations '
                              f'WHERE id == {meteostation_id};').fetchone()[0]
        if len(data) == 0:
            print(f"Data missing for {name} {year}")
            continue

        _, meteostation_id, date, temp = list(zip(*data))

        plt.plot(temp, label=name)

    plt.legend()

    plt.savefig(EXPORTS_FOLDER + '/' + f"temp_{year}_meteostations.png")


if __name__ == '__main__':
    connection, cursor = setup_db_connection()
    # for year in range(1970, 2000):
    #     plt.figure()
    #     plot_temp_by_year(cursor, year)

    plot_temp_by_meteostation(cursor, 15, start=2004, end=2019)
    plt.show()
