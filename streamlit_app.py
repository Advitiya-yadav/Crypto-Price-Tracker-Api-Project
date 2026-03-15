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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        data = r.json()

        if coin_id not in data:
            st.error(f"Could not fetch data for {coin_name}. CoinGecko may be rate limiting. Try again in a moment.")
        else:
            price = data[coin_id][currency]
            change_key = f"{currency}_24h_change"
            change = round(data[coin_id].get(change_key, 0), 2)

            st.metric(
                label=f"{coin_name} price",
                value=f"{price} {currency.upper()}",
                delta=f"{change}%"
            )
    except Exception as e:
        st.error(f"Error fetching data: {e}")