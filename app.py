from flask import Flask
from src.get_data import fetch_data, compute_date_information

app = Flask(__name__)

data = fetch_data()
data = compute_date_information(data)

@app.route('/')
def home():
    return "Hola mundo"

@app.route('/all_data')
def get_all_data():
    return data

if __name__ == "__main__":
    app.run()