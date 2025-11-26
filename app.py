from flask import Flask, request, jsonify
from alpha_vantage.timeseries import TimeSeries
import os
import pandas as pd

app = Flask(__name__)

# Your Alpha Vantage API key
ALPHA_VANTAGE_KEY = "8WFCXY8TJTSQHSDA"
ts = TimeSeries(key=ALPHA_VANTAGE_KEY, output_format='pandas')

@app.route("/get_stock", methods=["POST"])
def get_stock():
data = request.get_json()
symbol = data.get("symbol")

if not symbol:
return jsonify({"error": "No symbol provided"}), 400

try:
# Fetch intraday data (latest available)
stock_data, meta_data = ts.get_quote_endpoint(symbol)
stock_data = stock_data.to_dict()

current_price = stock_data['05. price']
open_price = stock_data['02. open']
high_price = stock_data['03. high']
low_price = stock_data['04. low']
previous_close = stock_data['08. previous close']
change_percent = stock_data['10. change percent']

human_readable = f"{symbol.upper()} - Current Price: ${current_price} (Change: {change_percent})\nOpen: ${open_price} High: ${high_price} Low: ${low_price} Previous Close: ${previous_close}"

response = {
"symbol": symbol.upper(),
"current_price": current_price,
"open": open_price,
"high": high_price,
"low": low_price,
"previous_close": previous_close,
"change_percent": change_percent,
"human_readable": human_readable
}

return jsonify(response)

except Exception as e:
return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
app.run(host="0.0.0.0", port=8080)
