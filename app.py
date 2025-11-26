from flask import Flask, request, jsonify
from alpha_vantage.timeseries import TimeSeries
import os

app = Flask(__name__)

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

ts = TimeSeries(
key=ALPHA_VANTAGE_API_KEY,
output_format="json"
)

@app.route("/", methods=["GET"])
def health_check():
return jsonify({"status": "Stock Fetcher running"}), 200

@app.route("/get_stock", methods=["POST"])
def get_stock():
try:
data = request.get_json()
symbol = data.get("symbol")

if not symbol:
return jsonify({"error": "Symbol is required"}), 400

stock_data, meta = ts.get_quote_endpoint(symbol)

price = float(stock_data["05. price"])
last_updated = meta.get("3. Last Refreshed")

return jsonify({
"symbol": symbol.upper(),
"source": "Alpha Vantage",
"current_price": price,
"last_updated": last_updated,
"currency": "USD",
"human_readable": f"{symbol.upper()} current price: ${price:.2f} (Alpha Vantage)"
})

except Exception as e:
return jsonify({"error": str(e)}), 500
