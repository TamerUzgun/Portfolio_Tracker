from django.shortcuts import render
from .models import Stock
import yfinance as yf
import plotly.graph_objs as go
from plotly.offline import plot

def portfolio_view(request):
    stocks = Stock.objects.all()
    portfolio = []

    total_value = 0
    total_cost = 0
    for stock in stocks:
        ticker = yf.Ticker(stock.symbol)
        current_price = ticker.history(period="1d")['Close'][0]
        current_value = current_price * stock.quantity
        cost = stock.purchase_price * stock.quantity
        total_value += current_value
        total_cost += cost
        portfolio.append({
            'symbol': stock.symbol,
            'quantity': stock.quantity,
            'purchase_price': stock.purchase_price,
            'current_price': current_price,
            'current_value': current_value,
            'cost': cost,
            'return': (current_value - cost) / cost * 100,
        })

    labels = [p['symbol'] for p in portfolio]
    sizes = [p['current_value'] for p in portfolio]

    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=.3)])
    fig.update_traces(textinfo='percent+label', pull=[0.1]*len(labels))
    fig.update_layout(title=' ', height=600)

    plot_div = plot(fig, output_type='div', include_plotlyjs=True)

    context = {
        'portfolio': portfolio,
        'total_value': total_value,
        'total_cost': total_cost,
        'plot_div': plot_div,
    }
    return render(request, 'portfolio/portfolio.html', context)
