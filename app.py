from flask import Flask, request, jsonify
from alpha_vantage.timeseries import TimeSeries
import os

app = Flask(__name__)

ALPHA_KEY = "8WFCXY8TJTSQHSDA"

@app.route("/get_stock", methods=["POST"])
def get_stock_data():
data = request.get_json()
symbol = data.get("symbol")

ts = TimeSeries(key=ALPHA_KEY, output_format='json')
stock_data, meta_data = ts.get_quote_endpoint(symbol)
current_price = float(stock_data['05. price'])

response_json = {
"symbol": symbol,
"current_price": current_price,
"raw_data": stock_data
}

human_readable = f"{symbol} current price: ${current_price:.2f}"

