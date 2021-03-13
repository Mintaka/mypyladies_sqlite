import data_sources
import process_meteo_data

def get_daily_average_temperatures(cursor, date_from=None, date_to=None, meteostations=None, limit=None):
    date_from_list = list(map(int, date_from.split(".")))
    date_to_list = list(map(int, date_to.split(".")))
    daily = cursor.execute(f"""SELECT * FROM temperatures
                                WHERE day BETWEEN {date_from_list[0]} AND {date_to_list[0]}
                                AND month BETWEEN {date_from_list[1]} AND {date_to_list[1]}
                                AND year BETWEEN {date_from_list[2]} and {date_to_list[2]}
                                ORDER BY year;""")
    daily_result = daily.fetchall()
    return daily_result

def get_yearly_average_temperatures(cursor, year_from=None, year_to=None, meteostations=None, limit=None):
    #make years ints
    years = []
    results = {}
    count_years = year_from
    for rok in range((year_to - year_from) + 1):
        years.append(count_years)
        count_years += 1
    i = 0
    for rok in years:
        query = cursor.execute(f"""SELECT Avg(temperature) FROM temperatures
        WHERE year LIKE {years[i]}""")
        results[f"{years[i]}"] = query.fetchall()
        i += 1
    return results

#print(get_daily_average_temperatures(cursor, date_from = "1.1.1991", date_to = "1.1.1993"))
