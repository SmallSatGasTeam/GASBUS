import sqlite3
from src.GASBUS_flight_logic.model import Model

class TestModel:
    def test__check_connection(self):
        assert type(Model._Model__check_connection(-10, -10)) == sqlite3.Connection