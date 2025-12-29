from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
#default for all Flask applications

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
#API endpoint of coingecko to get the simple price of cryptocurrencies

@app.route("/")
def home():
    return jsonify({"status": "API running"})
#Health check endpoint to verify if the API is running or not

@app.route("/price", methods=["GET"])
def price():
    coin = request.args.get("coin")
    currency = request.args.get("currency", "usd")
    #In this it is getting the coin and currency parameters from the request, with a default value of "usd" for currency if not provided

    if not coin:
        return jsonify({"error": "coin parameter is required"}), 400
    #similar to a security check if coin parameter is missing then it will return an error with status code 400 instead of crashing the app

    param = {
        "ids": coin,
        "vs_currencies": currency,
        "include_24hr_change": "true"
    }
    # This maps coingecko api requested parameters to our parameters using the params dictionary

    r = requests.get(COINGECKO_URL, params=param)
    #here we make a get request from the given api line ( coingecko url) and input the given parameters it then converts those parameters into valid query parameters which it enters
    
    data = r.json()
    #converts the response from the api from json format into python dictionary format which it got from the HTTP response, and stores into data variable

    if coin not in data:
        return jsonify({"error": "coin not found"}), 404
    #now it checks if coin is in the data dictionary or not , if not there then returns error coin not found with status code 404

    return jsonify({
        "coin": coin,
        "currency": currency,
        "price": data[coin][currency],
        "change_24h": round(data[coin][f"{currency}_24h_change"], 2)
    })
    # now we extract the price and 24 hour change from the data python dictionary and return it as a json responsestill

if __name__ == "__main__":
    app.run(debug=True)
