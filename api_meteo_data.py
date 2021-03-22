import data_sources
import process_meteo_data
import sqlite3
import pathlib
from process_meteo_data import setup_db_connection


def get_daily_average_temperatures(cursor, date_from=None, date_to=None, meteostations=None, limit=None):
    """
    This function takes starting date,end date in format YYYY-MM-DD and meteostation ID and returns daily average temperatures in that particular station between selected dates.
    If meteostation is not specified returns data from all of them.
    """
    if meteostations == None:
        daily = cursor.execute(f"""SELECT date,temperature FROM temperatures
                                    WHERE date BETWEEN '{date_from}' AND '{date_to}';""")
        daily_result = daily.fetchall()
    else:
        daily = cursor.execute(f"""SELECT meteostation_id,date,temperature FROM temperatures
                                    WHERE date BETWEEN '{date_from}' AND '{date_to}'
                                    AND meteostation_id = {meteostations};""")
        daily_result = daily.fetchall()
    return daily_result

def get_yearly_average_temperatures(cursor, date_from=None, date_to=None, meteostations=None, limit=None):
    """    
    This function takes starting date,end date (in format YYYY-MM-DD) and meteostation ID and returns yearly average temperatures in that particular station between selected dates.
    If meteostation is not specified returns data from all of them.
    Returned is dictionary {"year": average_temp}
    """
    #filter only years and make them int
    date_from_y = int(list(date_from.split("-"))[0])
    date_to_y = int(list(date_to.split("-"))[0])

    years = []
    results = {}
    count_years = date_from_y

    for rok in range((date_to_y - date_from_y) + 1): #create list called "years" which consist of range of years from selected dates (eg 1995-05-4 and 1998-04-09 creates years[1995, 1996, 1997, 1998])
        years.append(count_years)
        count_years += 1

    if meteostations == None:
        for rok in range(0, len(years)):
            query = cursor.execute(f"""SELECT Avg(temperature) FROM temperatures
            WHERE date LIKE '{years[rok]}%'""")
            avg_temp = query.fetchall()
            results[years[rok]] = float("%0.2f"%avg_temp[0][0])
    else:
        try:
            for rok in range(0, len(years)):
                query = cursor.execute(f"""SELECT Avg(temperature) FROM temperatures
                WHERE date LIKE '{years[rok]}%'
                AND meteostation_id = {meteostations};""")
                avg_temp = query.fetchall()
                results[years[rok]] = float("%0.2f"%avg_temp[0][0])
        except TypeError:
            print("Limited data for this meteostation in selected time frame!")
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
           for month in range(date_from_m,date_to_m + 1):
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

  ### Rozpracovane
def get_weekly_average_temperatures(cursor, date_from=None, date_to=None, meteostations=None, limit=None):
    daily = cursor.execute(f"""SELECT date,temperature FROM temperatures
                                WHERE date BETWEEN '{date_from}' AND '{date_to}';""")
    daily_result = daily.fetchall()
    date = [result [0] for result in daily_result]
    temp = [result [1] for result in daily_result]


    date_split = [tuple(map(int, item.split('-'))) for item in date]
    date_temp = [date_split, temp]
    print(date_temp)    
        
    return date_temp          

if __name__ == '__main__':
    connection, cursor = setup_db_connection()
    #print(get_daily_average_temperatures(cursor, date_from = "1995-05-15", date_to = "1996-06-30"))
    #print(get_yearly_average_temperatures(cursor, date_from = "1995-05-15", date_to = "1999-06-30", meteostations = 5))
    #print(get_monthly_average_temperatures(cursor, date_from = "1995-05-15", date_to = "1995-07-30"))
    #print(get_weekly_average_temperatures(cursor, date_from = "1995-05-15", date_to = "1995-06-15"))
    pass
