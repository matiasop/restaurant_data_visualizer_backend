from flask import Flask, render_template_string
from flask_cors import CORS
from get_data import fetch_data, compute_date_information
from filter_data import get_total_sales, get_sales_per_category, get_sales

app = Flask(__name__)
CORS(app)

data = fetch_data()
data = compute_date_information(data)


@app.route('/')
def home():
    return "Aplicación de Visualización de Datos de Restaurant"


@app.route('/all_data')
def get_all_data():
    return data


@app.route('/total_sales/<group>')
def total_sales(group):
    if group in ["month", "weekday"]:
        aggregator = "category"
    elif group in ["zone", "waiter", "cashier", "table"]:
        aggregator = "payment_type"
    else:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404')

    return get_total_sales(group, data, aggregator)


@app.route('/sales_per_category/<period>/<category>')
def sales_per_category(period, category):
    if period not in ["month", "weekday"]:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404')

    return get_sales_per_category(data, period, category)


@app.route('/doughnut_chart_data/<group>')
def doughnut_chart_data(group):
    if group not in ["weekday", "month", "zone", "waiter", "cashier", "table"]:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404')
    return get_sales(group, data)


if __name__ == "__main__":
    app.run()
