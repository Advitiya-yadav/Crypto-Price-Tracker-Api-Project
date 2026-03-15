import streamlit as st
import requests

st.title("🪙 Crypto Price Tracker")

COIN_SYMBOLS = {
    "Bitcoin": "BTCUSDT",
    "Ethereum": "ETHUSDT",
    "Solana": "SOLUSDT",
    "XRP": "XRPUSDT",
    "Cardano": "ADAUSDT",
    "Dogecoin": "DOGEUSDT",
    "Polkadot": "DOTUSDT",
    "Avalanche": "AVAXUSDT",
    "Tron": "TRXUSDT",
    "Polygon": "MATICUSDT",
    "Litecoin": "LTCUSDT",
    "Chainlink": "LINKUSDT",
    "Uniswap": "UNIUSDT",
    "Shiba Inu": "SHIBUSDT"
}

CURRENCY_RATES = {
    "USD": 1,
    "INR": 83.5,
    "EUR": 0.92
}

coin_name = st.selectbox("Enter coin name", list(COIN_SYMBOLS.keys()))
currency = st.selectbox("Select Currency", ["USD", "INR", "EUR"])

if st.button("Get Price"):
    symbol = COIN_SYMBOLS[coin_name]
    
    try:
        r = requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}", timeout=10)
        data = r.json()

        price_usd = float(data["lastPrice"])
        change = round(float(data["priceChangePercent"]), 2)
        rate = CURRENCY_RATES[currency]
        price = round(price_usd * rate, 2)

        st.metric(
            label=f"{coin_name} price",
            value=f"{price} {currency}",
            delta=f"{change}%"
        )
    except Exception as e:
        st.error(f"Error fetching data: {e}")