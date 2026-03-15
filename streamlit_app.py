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
    "Avalanche": "avalanche-2",
    "Tron": "tron",
    "Polygon": "matic-network",
    "Litecoin": "litecoin",
    "Chainlink": "chainlink",
    "Uniswap": "uniswap",
    "Shiba Inu": "shiba-inu"
}

coin_name = st.selectbox("Enter coin name", list(COIN_IDS.keys()))
currency = st.selectbox("Select Currency", ["USD", "INR", "EUR"]).lower()

if st.button("Get Price"):
    coin_id = COIN_IDS[coin_name]
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": currency,
        "include_24hr_change": "true"
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        price = data[coin_id][currency]
        change = round(data[coin_id][f"{currency}_24h_change"], 2)

        st.metric(
            label=f"{coin_name} price",
            value=f"{price} {currency.upper()}",
            delta=f"{change}%"
        )
    except Exception as e:
        st.error(f"Error fetching data: {e}")