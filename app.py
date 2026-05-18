from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BINANCE_URL = "https://api.binance.com/api/v3/ticker/24hr"


@app.route("/")
def home():
    return jsonify({"status": "API running"})


@app.route("/price", methods=["GET"])
def price():
    symbol = request.args.get("symbol", "").upper().strip()
    
    if not symbol:
        return jsonify({"error": "symbol parameter is required (e.g., BTCUSDT)"}), 400

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        r = requests.get(
            BINANCE_URL,
            params={"symbol": symbol},
            headers=headers,
            timeout=10
        )
        r.raise_for_status()
        data = r.json()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            return jsonify({"error": f"Invalid symbol: {symbol}"}), 400
        return jsonify({
            "error": "Failed to fetch data from Binance",
            "status_code": e.response.status_code
        }), 500
    except requests.exceptions.Timeout:
        return jsonify({"error": "Binance API request timed out"}), 503
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Connection error. Binance API unreachable"}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to fetch data from Binance",
            "details": str(e)
        }), 500

    try:
        return jsonify({
            "symbol": symbol,
            "price": float(data["lastPrice"]),
            "change_24h_percent": round(float(data["priceChangePercent"]), 2),
            "high_24h": float(data["highPrice"]),
            "low_24h": float(data["lowPrice"]),
            "volume": float(data["volume"])
        })
    except KeyError as e:
        return jsonify({"error": f"Missing expected field: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)