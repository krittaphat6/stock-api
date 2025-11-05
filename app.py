from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    return "Stock API พร้อมใช้งานแล้ว!"

@app.route('/stockinfo', methods=['GET'])
def stock_info():
    symbol = request.args.get('symbol', default='AAPL', type=str)
    stock = yf.Ticker(symbol)

    financials = stock.financials
    stock_data = stock.info

    latest_eps = stock_data.get("trailingEps", "N/A")
    pe_ratio = stock_data.get("trailingPE", "N/A")
    revenue = financials.loc["Total Revenue"][0] if "Total Revenue" in financials.index else "N/A"
    net_income = financials.loc["Net Income"][0] if "Net Income" in financials.index else "N/A"

    return jsonify({
        "symbol": symbol,
        "revenue": f"{revenue:,}" if isinstance(revenue, (int, float)) else revenue,
        "net_income": f"{net_income:,}" if isinstance(net_income, (int, float)) else net_income,
        "eps": latest_eps,
        "pe_ratio": pe_ratio,
        "message": f"ดึงข้อมูลหุ้น {symbol} เสร็จแล้ว"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
