import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

# Başlık
st.title('Portfolio Tracker')

# Kenar çubuğunda veri girişi için tablo oluşturma
st.sidebar.header('Portfolio Inputs')

# Veri girişi için başlangıç verilerini içeren DataFrame oluşturma
num_stocks = st.sidebar.number_input('Number of Stocks', min_value=1, max_value=10, value=5)

data = {
    'Stock Symbol': ['alark.is', 'try=x', 'tuprs.is', 'adel.is', 'akbnk.is'][:num_stocks],
    'Quantity': [123, 500, 100, 50, 200][:num_stocks],
    'Purchase Price': [115.00, 30.00, 150.00, 450.00, 50.00][:num_stocks]
}

df_input = pd.DataFrame(data)

# Kullanıcıdan veri girişi almak için editable DataFrame bileşeni
df_input = st.sidebar.data_editor(df_input, num_rows="dynamic")

# Portfolio verilerini işleme ve güncel fiyatları alma
portfolio_data = []
total_value = 0
total_cost = 0

for index, row in df_input.iterrows():
    symbol = row['Stock Symbol']
    quantity = row['Quantity']
    purchase_price = row['Purchase Price']

    ticker = yf.Ticker(symbol)
    current_price = ticker.history(period="1d")['Close'][0]
    current_value = current_price * quantity
    cost = purchase_price * quantity
    total_value += current_value
    total_cost += cost
    return_percentage = ((current_value - cost) / cost * 100) if cost != 0 else 0

    portfolio_data.append([
        symbol,
        quantity,
        f"{purchase_price:.4f}",
        round(current_price, 2),
        round(current_value, 2),
        round(cost, 2),
        round(return_percentage, 2)
    ])

# Portfolio tablosunu gösterme
st.header('Portfolio Overview')

# DataFrame oluşturma
df_portfolio = pd.DataFrame(portfolio_data, columns=[
    'Symbol', 'Quantity', 'Purchase Price', 'Current Price', 'Current Value', 'Cost', 'Return (%)'
])

# Tabloyu gösterme
st.table(df_portfolio)

# Portfolio dağılımı için pie chart oluşturma
labels = df_portfolio['Symbol']
sizes = df_portfolio['Current Value']

fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=.3)])
fig.update_traces(textinfo='percent+label', pull=[0.1] * len(labels))
fig.update_layout(title='Portfolio Distribution', height=600)

st.plotly_chart(fig)

# Genel değerleri gösterme
st.header('Total Values')
st.write(f'Total Value: {round(total_value, 2)}')
st.write(f'Total Cost: {round(total_cost, 2)}')
st.write(f'Profit %: {round(100*((total_value/total_cost)-1),2)}')
