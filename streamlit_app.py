import streamlit as st
import requests
import json

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
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        
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
        
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error: {e.response.status_code} - {e}")
    except requests.exceptions.Timeout:
        st.error("Request timed out. Binance API not responding.")
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Check your internet or try again.")
    except ValueError as e:
        st.error(f"Invalid data format from API: {e}")
    except Exception as e:
        st.error(f"Error fetching data: {e}")