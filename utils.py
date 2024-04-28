from exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError
from datetime import datetime


def data_processing(data):

    if data["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")

    first_cup_year = int(data["first_cup"].split("-")[0])

    if first_cup_year < 1930 or not first_cup_year % 4 == 2:
        raise InvalidYearCupError("there was no world cup this year")

    date_now = int(datetime.now().strftime("%Y"))

    if data["titles"] * 4 > (date_now - first_cup_year):
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
