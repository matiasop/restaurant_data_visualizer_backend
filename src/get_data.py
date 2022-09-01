import requests
from datetime import datetime


def fetch_data():
    url = "https://storage.googleapis.com/backupdatadev/ejercicio/ventas.json"

    response = requests.get(url)
    data = response.json()
    return data


def get_category(category, data):
    return list(set(map(lambda x: x[category], data)))


def get_datetime(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")


def get_duration(initial, final):
    duration = (final - initial).total_seconds() / 60
    return duration


def compute_weekday(date):
    weekdays = {0: "Lunes", 1: "Martes", 2: "Miércoles",
                3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
    return weekdays[date.weekday()]


def compute_month(date):
    months = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
              7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
    return months[date.month]


def compute_date_information(data):
    for order in data:
        initial = get_datetime(order["date_opened"])
        final = get_datetime(order["date_closed"])
        duration = get_duration(initial, final)
        weekday = compute_weekday(final)
        month = compute_month(final)
        order["duration"] = duration
        order["weekday"] = weekday
        order["month"] = month
    return data
