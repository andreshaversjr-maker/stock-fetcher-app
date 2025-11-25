from flask import Flask, request, jsonify
import yfinance as yf
from datetime import datetime

app = Flask(__name__)

@app.route("/stock", methods=["GET"])
def get_stocks():
tickers = request.args.get("tickers")
if not tickers:
return jsonify({"error": "Please provide tickers, e.g., ?tickers=AAPL,NFLX"})

tickers = tickers.split(",")
result = {}

for t in tickers:
stock = yf.Ticker(t)
data = stock.history(period="1d")
latest = data.iloc[-1]
result[t] = {
"symbol": t,
"company_name": stock.info.get("longName", t),
"current_price": latest['Close'],
"open": latest['Open'],
"high": latest['High'],
"low": latest['Low'],
"change_percent": ((latest['Close'] - latest['Open']) / latest['Open']) * 100,
"timestamp": datetime.now().isoformat()
}
return jsonify(result)

if __name__ == "__main__":
app.run(host="0.0.0.0", port=8080)
