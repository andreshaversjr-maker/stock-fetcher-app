from flask import Flask, request, jsonify
import yfinance as yf
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def home():
return "Stock Fetcher is running!"

@app.route("/stock", methods=["GET"])
def get_stock():
# Get ticker symbol from query parameter
symbol = request.args.get("symbol")
if not symbol:
return jsonify({"error": "Please provide a stock symbol, e.g., ?symbol=AAPL"}), 400

try:
stock = yf.Ticker(symbol)
data = stock.history(period="1d")
latest = data.iloc[-1]

result = {
"symbol": symbol.upper(),
"company_name": stock.info.get("longName", symbol.upper()),
"current_price": float(latest['Close']),
"open": float(latest['Open']),
"high": float(latest['High']),
"low": float(latest['Low']),
"previous_close": float(latest['Close']),
"change_percent": round(((latest['Close'] - latest['Open']) / latest['Open']) * 100, 2),
"volume": int(latest['Volume']),
"market_cap": stock.info.get("marketCap", None),
"fifty_two_week_high": stock.info.get("fiftyTwoWeekHigh", None),
"fifty_two_week_low": stock.info.get("fiftyTwoWeekLow", None),
"timestamp": datetime.utcnow().isoformat() + "Z"
}

# Human-readable summary
human_summary = f"{result['symbol']} – {result['company_name']}\n" \
f"Current price: ${result['current_price']} ({result['change_percent']}%)\n" \
f"Day range: ${result['low']} – ${result['high']}\n" \
f"Market cap: {result['market_cap']}\n" \
f"Updated: {result['timestamp']}"

return jsonify({
"json": result,
"human_readable": human_summary
})

except Exception as e:
return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)
