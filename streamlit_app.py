import streamlit as st
import requests

st.title("🪙 Crypto Price Tracker")

coin = st.selectbox("Enter coin name", 
                    [
                        "Bitcoin", "Ethereum", "Solana", "XRP", "Cardano","Dogecoin", "Tether",
                        "Polkadot", "Avalanche", "Tron", "Polygon","Litecoin", "Chainlink", "Uniswap", "Shiba Inu"
                    ]).lower().replace(" ", "-")
currency = st.selectbox("Select Currency",["USD", "INR", "EUR"]).lower()

if st.button("Get Price"):
    if coin == "":
        st.error("Please select a valid coin")
    else:
        url = "http://127.0.0.1:5000/price"
        params = {
            "coin": coin,
            "currency": currency
        }

        r = requests.get(url, params=params)
        data = r.json()

        if "error" in data:
            st.error(data["error"])
        else:
            st.metric(
                label=f"{coin.upper()} price",
                value=f"{data['price']} {currency.upper()}",
                delta=f"{data['change_24h']}%"
            )
