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

    results = {}
    
    if meteostations == None:
        for rok in range(date_from_y, date_to_y+1):
            query = cursor.execute(f"""SELECT Avg(temperature) FROM temperatures
            WHERE date LIKE '{rok}%'""")
            avg_temp = query.fetchall()
            results[rok] = float(avg_temp[0][0])
    else:
        try:
            for rok in range(date_from_y, date_to_y+1):
                query = cursor.execute(f"""SELECT Avg(temperature) FROM temperatures
                WHERE date LIKE '{rok}%'
                AND meteostation_id = {meteostations};""")
                avg_temp = query.fetchall()
                results[rok] = float(avg_temp[0][0])
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

def get_weekly_average_temperatures(cursor, date_from=None, date_to=None, meteostations = None , limit=None):
    import datetime
    from itertools import groupby
    
    # Database Query
    daily = cursor.execute(f"""SELECT meteostation_id,date,temperature FROM temperatures
                                    WHERE date BETWEEN '{date_from}' AND '{date_to}'
                                    AND meteostation_id = {meteostations};""")
    
    daily_result = daily.fetchall()
    
    # Initialization variables
    date_weekly = []
    week_group = []
    temp_av = [] 
    year_results = {}

    # Convert to date time format with week numbers
    for m_id, date, temp  in daily_result:
        date_reformat = datetime.datetime.strptime(date,"%Y-%m-%d")
        n_week = date_reformat.strftime("%W")
        n_year = date_reformat.strftime("%Y")
        
        date_weekly.append((n_year,n_week, temp))
      
     # Group data by weeks
    for key_week, group in groupby(date_weekly, lambda x: x[1]):
         week = list(group)
         week_group.append(week)
    
    # Calculate average temp for each week and add it to list     
    for item in week_group:
        t_sum = 0
        length = 0
        
        for temp in item:
            t_sum = t_sum + temp[2]
            length += 1
        temp_av.append((item[0][0],int(temp[1]), t_sum/length))
        
    # Group data by years 
    year_results = {}

    x = {}
    for year_key, group in groupby(temp_av, lambda x: x[0]):
        y = list(group)
        year_results.update({year_key: y})
    
    # Create dicionary of results 
    for key in year_results.keys():
            week_results = {}
            for week_key, group in groupby(year_results [key], lambda x: x[1]):
                y = list(group)
                week_results.update({week_key: y[0][2]})
            x [key] = week_results


if __name__ == '__main__':
    connection, cursor = setup_db_connection()
    #print(get_daily_average_temperatures(cursor, date_from = "1995-05-15", date_to = "1996-06-30"))
    #print(get_yearly_average_temperatures(cursor, date_from = "1995-05-15", date_to = "1999-06-30", meteostations=1))
    #print(get_monthly_average_temperatures(cursor, date_from = "1995-05-15", date_to = "1995-07-30"))
    #print(get_weekly_average_temperatures(cursor, date_from = "1995-05-15", date_to = "1995-06-15"))
    pass
