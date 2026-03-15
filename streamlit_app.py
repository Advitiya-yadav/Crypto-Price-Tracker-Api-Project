import streamlit as st
import requests

st.title("🪙 Crypto Price Tracker")

st.info("🔑 Get your free API key at [coingecko.com/en/api](https://www.coingecko.com/en/api) → Demo API Key (free, no credit card)")

api_key = st.text_input("Enter your CoinGecko API Key", type="password")

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
    if not api_key:
        st.warning("Please enter your CoinGecko API key first!")
    else:
        coin_id = COIN_IDS[coin_name]
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": currency,
            "include_24hr_change": "true"
        }
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": api_key
        }

        try:
            r = requests.get(url, params=params, headers=headers, timeout=10)
            data = r.json()

            if coin_id not in data:
                st.error("Invalid API key or rate limit hit. Double check your key!")
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