import streamlit as st
import yfinance as yf
import pandas as pd

# General Settings

PAGE_TITTLE = "Wartość portfela inwestycyjnego"
PAGE_ICON = ":wave:"

st.set_page_config(page_title=PAGE_TITTLE, page_icon=PAGE_ICON)

# funkcja pobierająca notowania kursów ze strony Yahoo Finance
def get_stock_price(row):
    symbol = row['Symbol']
    quantity = row['Ilość']
    if row['Rodzaj'] == 'GPW':
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        price = data['Close'][0]
    else:
        price = 1
    return price

st.write(":green[💻 Wczytaj dane z pliku Excel]")
uploaded_file = st.file_uploader("", type=["xlsx"])

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file, header=None, names=["Rodzaj", "Symbol", "Ilość"])
    st.write('#')
    st.write("✅ Dane z pliku CSV:")
    st.write(data)

    data["Kurs"] = data.apply(lambda row: get_stock_price(row), axis=1)
    data["Wartość"] = data["Ilość"] * data["Kurs"]
    
    st.write('#')
    st.write("📊 Wartość poszczególnych akcji w portfelu")
    for index, row in data.iterrows():
        st.write(f"{row['Symbol']} ➡️ {format(row['Wartość'], ',.2f').replace(',', ' ')} PLN")

    st.write('#')
    st.write("👉Wartość portfela inwestycyjnego👈")
    current_portfolio_value = data['Wartość'].sum()
    st.write(f"➡️ {format(current_portfolio_value, ',.2f').replace(',', ' ')} PLN")

    form = st.form(key='my-form')
    days = form.number_input('Wpisz liczbę dni na przestrzeni której zmieniła się wartość twojego portfela', value=30, min_value=1)
    submit_button = form.form_submit_button('Oblicz')

    if submit_button:
        def get_stock_price(row):
            symbol = row['Symbol']
            quantity = row['Ilość']
            if row['Rodzaj'] == 'GPW':
                ticker = yf.Ticker(symbol)
                data = ticker.history(period=f"{days+1}d")
                price = data['Close'][0]
            else:
                price = 1
            return price
        data["Kurs"] = data.apply(lambda row: get_stock_price(row), axis=1)
        data["Wartość"] = data["Ilość"] * data["Kurs"]
        last_portfolio_value = data['Wartość'].sum()
        percentage_change = (current_portfolio_value - last_portfolio_value) / current_portfolio_value * 100
        
        st.write(f"Zmiana wartości portfela na przestrzeni {days} dni:")
        st.write(f"🕵🏻 {format(current_portfolio_value - last_portfolio_value, ',.2f').replace(',', ' ')} PLN")
        st.write('#')
        st.write(f"Procentowa zmiana wartości portfela na przestrzeni {days} dni:")
        st.write(f"📊 {format(percentage_change, ',.2f')} %")