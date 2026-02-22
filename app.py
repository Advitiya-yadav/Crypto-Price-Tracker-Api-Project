from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


@app.route("/")
def home():
    return jsonify({"status": "API running"})


@app.route("/price", methods=["GET"])
def price():
    coin = request.args.get("coin", "").lower().strip()
    currency = request.args.get("currency", "usd").lower().strip()

    if not coin:
        return jsonify({"error": "coin parameter is required"}), 400

    params = {
        "ids": coin,
        "vs_currencies": currency,
        "include_24hr_change": "true"
    }

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(
            COINGECKO_URL,
            params=params,
            headers=headers,
            timeout=10
        )
        r.raise_for_status()
        data = r.json()

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to fetch data from CoinGecko",
            "details": str(e)
        }), 500

    if coin not in data:
        return jsonify({"error": "coin not found"}), 404

    try:
        return jsonify({
            "coin": coin,
            "currency": currency,
            "price": data[coin][currency],
            "change_24h": round(data[coin].get(f"{currency}_24h_change", 0), 2)
        })
    except KeyError:
        return jsonify({"error": "Invalid currency"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)