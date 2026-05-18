import streamlit as st
import requests
from datetime import datetime, timedelta

st.title("🪙 Crypto Price Tracker")

COIN_MAPPING = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "XRP": "ripple",
    "Cardano": "cardano",
    "Dogecoin": "dogecoin",
    "Polkadot": "polkadot",
    "Avalanche": "avalanche-2",
    "Tron": "tron",
    "Polygon": "matic-network",
    "Litecoin": "litecoin",
    "Chainlink": "chainlink",
    "Uniswap": "uniswap",
    "Shiba Inu": "shiba-inu"
}

@st.cache_data(ttl=300)
def fetch_price(coin_id, currency):
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": currency,
        "include_24hr_change": "true"
    }
    
    r = requests.get(url, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()

coin_name = st.selectbox("Enter coin name", list(COIN_MAPPING.keys()))
currency = st.selectbox("Select Currency", ["usd", "inr", "eur"])

if st.button("Get Price"):
    coin_id = COIN_MAPPING[coin_name]
    
    try:
        data = fetch_price(coin_id, currency)

        if coin_id not in data:
            st.error(f"Coin {coin_name} not found")
        else:
            price = data[coin_id].get(currency, 0)
            change = round(data[coin_id].get(f"{currency}_24h_change", 0), 2)

            st.metric(
                label=f"{coin_name} price",
                value=f"{price:,.2f} {currency.upper()}",
                delta=f"{change}%"
            )
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            st.error("Rate limited. Please wait a moment and try again.")
        else:
            st.error(f"HTTP Error: {e.response.status_code}")
    except requests.exceptions.Timeout:
        st.error("Request timed out. Try again.")
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Check your internet.")
    except Exception as e:
        st.error(f"Error fetching data: {e}")