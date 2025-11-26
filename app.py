@app.route("/get_stock", methods=["POST"])
def get_stock_data():
data = request.get_json()
symbol = data.get("symbol")

# Alpha Vantage API call
ts = TimeSeries(key='8WFCXY8TJTSQHSDA', output_format='json')
stock_data, meta_data = ts.get_quote_endpoint(symbol)
current_price = float(stock_data['05. price'])

# Build JSON and human-readable output
response_json = {
"symbol": symbol,
"current_price": current_price,
"raw_data": stock_data
}

human_readable = f"{symbol} current price: ${current_price:.2f}"

return jsonify({
"json": response_json,
"human_readable": human_readable
})
