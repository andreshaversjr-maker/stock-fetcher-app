from flask import Flask, request, jsonify
import yfinance as yf
from datetime import datetime

app = Flask(__name__)

def get_real_time_price(ticker):
stock = yf.Ticker(ticker)
data = stock.history(period="1d")
latest = data.iloc[-1]

return {
"symbol": ticker,
"company_name": stock.info.get("longName", ticker),
"current_price": latest['Close'],
"open": latest['Open'],
"high": latest['High'],
"low": latest['Low'],
"previous_close": latest['Close'],
"change_percent": ((latest['Close'] - latest['Open']) / latest['Open']) * 100,
"volume": int(latest['Volume']),
"market_cap": stock.info.get("marketCap", None),
"fifty_two_week_high": stock.info.get("fiftyTwoWeekHigh", None),
"fifty_two_week_low": stock.info.get("fiftyTwoWeekLow", None),
"timestamp": datetime.now().isoformat()
}

@app.route("/stock", methods=["GET"])
def get_stock():
symbol = request.args.get("symbol")
if not symbol:
return jsonify({"error": "Please provide a stock symbol using ?symbol=XYZ"}), 400

try:
stock_data = get_real_time_price(symbol.upper())
return jsonify(stock_data)
except Exception as e:
return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
app.run(host="0.0.0.0", port=8080)

