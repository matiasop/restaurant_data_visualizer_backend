from flask import Flask, render_template_string
from get_data import fetch_data, compute_date_information
from filter_data import get_total_sales

app = Flask(__name__)

data = fetch_data()
data = compute_date_information(data)


@app.route('/')
def home():
    return "Hola mundo"


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


if __name__ == "__main__":
    app.run()
