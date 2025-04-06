from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/stockinfo', methods=['GET'])
def stock_info():
    symbol = request.args.get('symbol', default='AAPL', type=str)
    stock = yf.Ticker(symbol)

    fin = stock.financials
    info = stock.info

    latest_eps = info.get("trailingEps", "N/A")
    pe_ratio = info.get("trailingPE", "N/A")
    revenue = fin.loc['Total Revenue'][0] if 'Total Revenue' in fin.index else "N/A"
    net_income = fin.loc['Net Income'][0] if 'Net Income' in fin.index else "N/A"

    return jsonify({
        "symbol": symbol,
        "revenue": f"{revenue:,}",
        "net_income": f"{net_income:,}",
        "eps": latest_eps,
        "pe_ratio": pe_ratio,
        "message": f"งบการเงิน {symbol} เรียบร้อย"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
