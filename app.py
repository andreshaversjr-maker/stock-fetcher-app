from flask import Flask, request, jsonify
from alpha_vantage.timeseries import TimeSeries
import os

# Initialize Flask app
app = Flask(__name__)

# Alpha Vantage API key (replace with your key)
ALPHA_VANTAGE_KEY = "8WFCXY8TJTSQHSDA"

@app.route("/")
def root():
return "Stock Fetcher API is running!"

@app.route("/get_stock", methods=["POST"])
def get_stock_data():
try:
data = request.get_json()
symbol = data.get("symbol")

if not symbol:
return jsonify({"error": "No symbol provided"}), 400

# Alpha Vantage API call
ts = TimeSeries(key=ALPHA_VANTAGE_KEY, output_format='json')
stock_data, meta_data = ts.get_quote_endpoint(symbol)
current_price = float(stock_data['05. price'])

# Build JSON response
response_json = {
"symbol": symbol,
"current_price": current_price,
"raw_data": stock_data
}

# Human-readable summary
human_readable = f"{symbol} current price: ${current_price:.2f}"

return jsonify({
"json": response_json,
"human_readable": human_readable
})

except Exception as e:
return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
# Cloud Run requires host=0.0.0.0 and port from env
port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)

