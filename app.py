from flask import Flask, request, jsonify
from alpha_vantage.timeseries import TimeSeries
import os
from datetime import datetime
import pytz # add this to requirements if not installed

app = Flask(__name__)

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

ts = TimeSeries(
key=ALPHA_VANTAGE_API_KEY,
output_format="json"
)

def infer_market_session(latest_trading_day_str):
"""
Very simple session guesser.
You can improve this later, but this is fine for v1.
"""
try:
eastern = pytz.timezone("US/Eastern")
now_et = datetime.now(eastern)

# Parse Alpha Vantage "latest trading day" (e.g. "2025-02-06")
latest_day = datetime.strptime(latest_trading_day_str, "%Y-%m-%d").date()
today = now_et.date()

# Weekend / closed
if latest_day < today:
return "Last Close"

# During regular hours (roughly 9:30–16:00 ET)
if now_et.hour < 9 or (now_et.hour == 9 and now_et.minute < 30):
return "Pre-Market (using last close)"
elif 9 <= now_et.hour < 16 or (now_et.hour == 16 and now_et.minute == 0):
return "Regular Session"
else:
return "After Hours (using latest available quote)"
except Exception:
return "Unknown Session"

@app.route("/get_stock", methods=["POST"])
def get_stock():
try:
data = request.get_json()
symbol = data.get("symbol")

if not symbol:
return jsonify({"error": "Symbol is required"}), 400

stock_data, meta = ts.get_quote_endpoint(symbol)

# Alpha Vantage GLOBAL_QUOTE style fields
price = float(stock_data["05. price"])
latest_trading_day = stock_data.get("07. latest trading day", "")
market_session = infer_market_session(latest_trading_day)

# Build response with context
response = {
"symbol": symbol.upper(),
"source": "Alpha Vantage",
"current_price": price,
"last_updated": latest_trading_day,
"currency": "USD",
"market_session": market_session,
"data_confidence": "Real-time pricing via Alpha Vantage (informational use only)",
"latency_note": "Prices may lag exchange quotes and broker prices by several minutes.",
"human_readable": f"{symbol.upper()} current price: ${price:.2f} ({market_session}, Alpha Vantage)"
}

return jsonify(response), 200

except Exception as e:
return jsonify({"error": str(e)}), 500
