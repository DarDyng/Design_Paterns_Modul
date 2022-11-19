import unittest
from random import randint
from main import *

class TestEmployee(unittest.TestCase):

    def test_transport_route_01(self):

        st1 = Station(1, "Львів", 49.948726, 23.543115)
        st2 = Station(2, "Київ", 49.921909, 23.731047)

        ps1 = ("Pedro", 123, st1.title, st2.title)
        ps2 = ("Ivan", 43, st1.title, st2.title)
        ps3 = ("Dimon", 23, st1.title, st2.title)
        ps4 = ("Pokemon", 54, st1.title, st2.title)

        all_ps = [ps1, ps2, ps3, ps4]

        tran1 = Bus(len(all_ps), 4500, 200, "Іван")

        a = Route()
        a.route_calculation(tran1, st1, st2, all_ps)

    def test_transport_route_02(self):

        st1 = Station(4, "Одеса", 49.948726, 23.543115)
        st2 = Station(5, "Тернопіль", 49.642179, 24.968033)

        ps1 = ("Pedro", 123, st1.title, st2.title)
        ps2 = ("Ivan", 43, st1.title, st2.title)
        ps3 = ("Dimon", 23, st1.title, st2.title)
        ps4 = ("Pokemon", 54, st1.title, st2.title)
        ps5 = ("Beatrice", 573, st1.title, st2.title)
        ps6 = ("Julian", 55, st1.title, st2.title)
        ps7 = ("Lynda", 77, st1.title, st2.title)
        ps8 = ("Seward", 87, st1.title, st2.title)

        all_ps = [ps1, ps2, ps3, ps4, ps5, ps6, ps7, ps8]

        tran1 = Train(len(all_ps), 15500, 1500, "Петро")

        a = Route()
        a.route_calculation(tran1, st1, st2, all_ps)


if __name__ == '__main__':
    unittest.main()