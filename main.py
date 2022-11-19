import json
import requests
from abc import ABC, abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import Dict
import sqlite3

my_key = "OAWljfmhlWNfiKLQbqKY3ZdNh3FSIKss"
decor = "=" + "-" * 50 + "="

class Info_Station:

    def __init__(self, station_id: int, title: str, lat, lon):
        """
        :param station_id: id станції
        :param title:      Назва станції
        :param lat:        Координата 1
        :param lon:        Координата 2
        """
        self.station_id = station_id
        self.title = title
        self.lat = lat
        self.lon = lon


class Station(Info_Station):

    def __init__(self, station_id: int, title: str, lat, lon):
        """
        :param station_id: id станції
        :param title:      Назва станції
        :param lat:        Координата 1
        :param lon:        Координата 2
        """
        self.station_id = station_id
        self.title = title
        self.lat = lat
        self.lon = lon


class Depo(Info_Station):

    def __init__(self, station_id: int, title: str, lat, lon):
        """
        :param station_id: id станції
        :param title:      Назва станції
        :param lat:        Координата 1
        :param lon:        Координата 2
        """
        self.station_id = station_id
        self.title = title
        self.lat = lat
        self.lon = lon



class Transport:

    def __init__(self, full_weight=0, driver_name=""):
        """
        :param full_weight: Повна вага
        :param driver_name: Імя водія
        """
        self.full_weight = full_weight
        self.driver = driver_name

        @property  # Getter full_weight
        def f_full_weight(self):
            return self.full_weight

        @f_full_weight.setter  # Setter full_weight
        def f_full_weight(self, filled_inp):
            self.full_weight = filled_inp

        @property  # Getter driver_name
        def f_driver_name(self):
            return self.driver_name

        @f_driver_name.setter  # Setter driver_name
        def f_driver_name(self, filled_inp):
            self.driver_name = filled_inp


class Bus(Transport):

    def __init__(self, number_passengers, weight_bus, cargo_weight, driver_name):
        """
        :param number_passengers: Кількість пасажирів
        :param weight_bus:        Вага буса
        :param cargo_weight:      Вага вантажа
        :param driver_name:       Імя водія
        """
        self.type = "Bus"
        self.number_passengers = number_passengers
        self.full_weight = weight_bus + number_passengers * 60 + cargo_weight
        self.driver = driver_name


class Train(Transport):

    def __init__(self, number_passengers, weight_train, cargo_weight, driver_name):
        """
        :param number_passengers: Кількість пасажирів
        :param weight_bus:        Вага буса
        :param cargo_weight:      Вага вантажа
        :param driver_name:       Імя водія
        """
        self.type = "Train"
        self.number_passengers = number_passengers
        self.full_weight = weight_train + number_passengers * 60 + cargo_weight
        self.driver = driver_name


class Truck(Transport):

    def __init__(self, number_passengers, weight_truck, cargo_weight, driver_name):
        """
        :param number_passengers: Кількість пасажирів
        :param weight_bus:        Вага буса
        :param cargo_weight:      Вага вантажа
        :param driver_name:       Імя водія
        """
        self.type = "Truck"
        self.number_passengers = number_passengers
        self.full_weight = weight_train + number_passengers * 60 + cargo_weight
        self.driver = driver_name


@dataclass
class Route_Data:
    """
    :param length_in_km:    Відстань в КМ
    :param travel_time_sec: Час подорожі в секундах
    :param departure_time:  Час початку руху
    :param arrival_time:    Час закінчення руху
    :param all_points:      Всі точки руху
    :param all_pessenger:   Всі пасажири
    """
    length_in_km: float = 0
    travel_time_sec: int = 0
    departure_time: str = "Not_data"
    arrival_time: str = "Not_data"
    all_points: Dict[int, list] = field(default_factory=lambda: {})
    all_pessenger: Dict[int, str] = field(default_factory=lambda: {})


class Route(Route_Data):


    def route_calculation(self, transport, station_a, station_b, passenger_list):
        """
        :param transport:      Транспорт
        :param station_a:      Перша станція(зупинка)
        :param station_b:      Остання станція(зупинка)
        :param passenger_list: Список пасажирів
        :return:
        """
        self.url_info = requests.get(
            f"https://api.tomtom.com/routing/1/calculateRoute/{station_a.lat},{station_a.lon}:{station_b.lat},{station_b.lon}/json?key={my_key}").text
        self.route_info = json.loads(self.url_info)

        try:
            self.length_in_km = int(self.route_info['routes'][0]['summary']['lengthInMeters']) / 1000
            self.travel_time_sec = int(self.route_info['routes'][0]['summary']['travelTimeInSeconds'])
            self.departure_time = self.route_info['routes'][0]['summary']['departureTime']
            self.arrival_time = self.route_info['routes'][0]['summary']['arrivalTime']

            for i in range(len(self.route_info['routes'][0]['legs'][0]['points'])):
                self.all_points[i + 1] = [float(self.route_info['routes'][0]['legs'][0]['points'][i]['latitude']),
                                          float(self.route_info['routes'][0]['legs'][0]['points'][i]['longitude'])]
        except:
            print("Халепа( Щось пішло не так у блоці з конвертації json")

        database = sqlite3.connect('logistics.db')  # Start
        logistics_db = database.cursor()

        logistics_db.execute("SELECT MAX(route_id) FROM routes;")
        output_main_id = logistics_db.fetchone()[0]

        if output_main_id == None:  # Перевірка на те чи є рядки в таблиці
            output_main_id = 1
        else:
            output_main_id += 1

        logistics_db.execute(f"""CREATE TABLE pessenger_route_{output_main_id} (
        name text,
        ticket text,
        start_point text,
        end_point text
        )""")

        logistics_db.execute(f"""CREATE TABLE points_route_{output_main_id} (
        point text,
        point_lat text,
        point_lon text
        )""")

        database.commit()  # End
        database.close()

        for i in range(len(passenger_list)):
            database = sqlite3.connect('logistics.db')  # Start
            logistics_db = database.cursor()

            logistics_db.execute(f"""INSERT INTO pessenger_route_{output_main_id} VALUES(
            '{passenger_list[i][0]}',
            '{passenger_list[i][1]}',
            '{passenger_list[i][2]}',
            '{passenger_list[i][3]}'
            )""")

            database.commit()  # End
            database.close()

        for i in range(len(self.all_points)):
            database = sqlite3.connect('logistics.db')  # Start
            logistics_db = database.cursor()

            logistics_db.execute(f"""INSERT INTO points_route_{output_main_id} VALUES(
            '{i + 1}',
            '{self.all_points[i + 1][0]}',
            '{self.all_points[i + 1][1]}'
            )""")

            database.commit()  # End
            database.close()

        database = sqlite3.connect('logistics.db')  # Start
        logistics_db = database.cursor()

        logistics_db.execute(f"""INSERT INTO routes VALUES(
{output_main_id},
{station_a.station_id},
'{station_a.title}',
{station_a.lat},
{station_a.lon},
{station_b.station_id},
'{station_b.title}',
{station_b.lat},
{station_b.lon},
{self.length_in_km},
{self.travel_time_sec},
'{self.departure_time}',
'{self.arrival_time}',
{output_main_id},
{output_main_id},
'{transport.type}',
{transport.number_passengers},
{transport.full_weight},
'{transport.driver}'
)""")
        database.commit()  # End
        database.close()

        print(decor)
        print(f"Розрахунок маршруту id якого: {output_main_id}")
        print(decor)
        self.print_info(transport)

    def print_info(self, transport):

        print(f"Час виїзду: {self.departure_time}")
        print(f"Час приїзду: {self.arrival_time}")

        time_in_run = ""
        if self.travel_time_sec < 60:
            time_in_run = str(self.travel_time_sec) + " Секунд"
        elif self.travel_time_sec > 60 and self.travel_time_sec < 3600:
            time_in_run = str(round(self.travel_time_sec / 60, 2)) + " Хвилин"
        elif self.travel_time_sec > 3600:
            time_in_run = str(round(self.travel_time_sec / 3600, 2)) + " Годин"

        print(f"Час в русі: {time_in_run}")
        print(f"Відстань: {round(self.length_in_km, 2)} км")
        print(f"Вид транспорту: {transport.type}")
        print(f"Вага транспорту з вантажом: {transport.full_weight}")
        print(f"Водій: {transport.driver}")
        print(f"Всі точки маршруту: {self.all_points}")
        print(decor)


class Pessenger:

    def __init__(self, name, ticket, point_a, point_b):
        """
        :param name: Імя
        :param ticket:  Квиток
        :param point_a: Пункт А   А ----> B
        :param point_b: Пункт Б
        """
        self.name = name
        self.ticket = ticket
        self.point_a = point_a
        self.point_b = point_b





