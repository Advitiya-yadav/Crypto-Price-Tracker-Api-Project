import streamlit as st
import requests

st.title("🪙 Crypto Price Tracker")

COIN_IDS = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "XRP": "ripple",
    "Cardano": "cardano",
    "Dogecoin": "dogecoin",
    "Tether": "tether",
    "Polkadot": "polkadot",
    "Avalanche": "avalanche",
    "Tron": "tron",
    "Polygon": "polygon",
    "Litecoin": "litecoin",
    "Chainlink": "chainlink",
    "Uniswap": "uniswap",
    "Shiba Inu": "shiba-inu"
}

coin_name = st.selectbox("Enter coin name", list(COIN_IDS.keys()))
currency = st.selectbox("Select Currency", ["USD", "INR", "EUR"]).lower()

CURRENCY_RATES = {
    "usd": 1,
    "inr": 83.5,
    "eur": 0.92
}

if st.button("Get Price"):
    coin_id = COIN_IDS[coin_name]
    url = f"https://api.coincap.io/v2/assets/{coin_id}"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        if "data" not in data:
            st.error("Could not fetch data. Try again!")
        else:
            price_usd = float(data["data"]["priceUsd"])
            change = round(float(data["data"]["changePercent24Hr"]), 2)
            rate = CURRENCY_RATES[currency]
            price = round(price_usd * rate, 2)

            st.metric(
                label=f"{coin_name} price",
                value=f"{price} {currency.upper()}",
                delta=f"{change}%"
            )
    except Exception as e:
        st.error(f"Error fetching data: {e}")