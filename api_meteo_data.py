import data_sources
import process_meteo_data
import sqlite3
import pathlib
from process_meteo_data import setup_db_connection



#date: YYYY-MM-DD
def get_daily_average_temperatures(cursor, date_from=None, date_to=None, meteostations=None, limit=None):
    daily = cursor.execute(f"""SELECT date,temperature FROM temperatures
                                WHERE date BETWEEN '{date_from}' AND '{date_to}';""")
    daily_result = daily.fetchall()
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
        results[f"{years[i]}"] = avg_temp[2:5] #for every year get average temperature and put it into the dictionary as string
        i += 1
    return results

def get_monthly_average_temperatures(cursor, date_from=None, date_to=None, meteostations=None, limit=None):
    date_from_y = int(list(date_from.split("-"))[0])
    date_to_y = int(list(date_to.split("-"))[0])
    
    date_from_m = int(list(date_from.split("-"))[1])
    date_to_m = int(list(date_to.split("-"))[1])

    year_month = {}
    results_month = {}
    results = {}
    year_actuall = date_from_y

    while year_actuall != date_to_y + 1:
        
        if date_from_y == date_to_y:
           months = {}
           count_months = date_from_m
           for month in range(date_to_m,date_to_m + 1):
               months [month] = "NaN"
               count_months += 1
           year_month [year_actuall] = months 
        
        if (year_actuall == date_from_y) and date_from_y != date_to_y:
            months = {}
            count_months = date_from_m
            for month in range(date_from_m,13):
                months [month] = "NaN"
                count_months += 1
            year_month [year_actuall] = months
                
        elif year_actuall == date_to_y:
            months = {}
            count_months = 1
            for month in range(1,date_to_m + 1):
                months [month] = "NaN"
                count_months += 1
            year_month [year_actuall] = months
            
        else:
            months = {}
            for month in range(1,13):
                months [month] = "NaN"             
            year_month [year_actuall] = months
        
        year_actuall += 1

    for k,v in year_month.items():
        results_month = {}
        for i in v.keys(): 
            query = cursor.execute(f"""SELECT Avg(temperature) FROM temperatures
                                    WHERE date LIKE '{k}-%{i}%'""")
            avg_temp = str(query.fetchall())
            results_month [i] = avg_temp[2:7]
        results [k] = results_month
    return results
            

if __name__ == '__main__':
    connection, cursor = setup_db_connection()
    # print(get_yearly_average_temperatures(cursor, date_from = "1995-05-15", date_to = "1999-06-30"))
    # print(get_monthly_average_temperatures(cursor, date_from = "1995-05-15", date_to = "1995-07-30"))
    pass
