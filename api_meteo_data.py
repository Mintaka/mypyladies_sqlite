import data_sources
import process_meteo_data
import sqlite3
import pathlib
from process_meteo_data import setup_db_connection



#date: YYYY-MM-DD
def get_daily_average_temperatures(cursor, date_from=None, date_to=None, meteostations=None, limit=None):
    daily = cursor.execute(f"""SELECT * FROM temperatures
                                WHERE date BETWEEN '{date_from}' AND '{date_to}';""")
    daily_result = daily.fetchall()
    #bez ID (option True/False)
    return daily_result

def get_yearly_average_temperatures(cursor, date_from=None, date_to=None, meteostations=None, limit=None):
    #filter only years and make them int
    date_from_y = int(list(date_from.split("-"))[0])
    date_to_y = int(list(date_to.split("-"))[0])

    years = []
    results = {}
    count_years = date_from_y
    for rok in range((date_to_y - date_from_y) + 1): #create list called "years" which consist of range of years from selected dates (eg 1995-05-4 and 1998-04-09 creates years[1995, 1996, 1997, 1998])
        years.append(count_years)
        count_years += 1

    i = 0
    for rok in years:
        query = cursor.execute(f"""SELECT Avg(temperature) FROM temperatures
        WHERE date LIKE '{years[i]}%'""")
        avg_temp = str(query.fetchall())
        results[f"{years[i]}"] = avg_temp[2:-3] #for every year get average temperature and put it into the dictionary as string
        i += 1
    return results

#print(get_yearly_average_temperatures(cursor, date_from = "1995-05-15", date_to = "1999-06-30"))

if __name__ == '__main__':
    connection, cursor = setup_db_connection()
    pass