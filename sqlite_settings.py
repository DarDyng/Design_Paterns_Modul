import sqlite3

"""
Створоення і очищення таблиці з назвою routes
"""
truthfulness_01 = True


database = sqlite3.connect('logistics.db')  # Start
logistics_db = database.cursor()

if truthfulness_01:

    # logistics_db.execute("DROP TABLE routes")

    logistics_db.execute("""CREATE TABLE routes (
    route_id integer,
    id_start_station integer,
    title_start_station text,
    lat_start_station real,
    lon_start_station real,
    id_end_station integer,
    title_end_station text,
    lat_end_station real,
    lon_end_station real,
    length_in_km real,
    travel_time_sec real,
    departure_time text,
    arrival_time text,
    all_points_id integer,
    all_pessenger_id integer,
    transport_type text,
    number_passengers integer,
    full_weight real,
    driver_name text
    )""")


database.commit()  # End
database.close()