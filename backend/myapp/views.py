from django.shortcuts import render
from iexfinance.stocks import Stock, get_historical_data
from django.shortcuts import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime
import json

IEX_API_TOKEN = 'pk_5285253cdc634617bde2f7c4d153ee23'


def index(request):
    search_term = ''
    if 'search' in request.GET:
        pd.set_option('display.max_columns', None)
        search_term = request.GET['search']
        stock = Stock(search_term, token=IEX_API_TOKEN)
        img = stock.get_logo()
        df = stock.get_quote()
        company = stock.get_company()
        html = []
        html = df[['change', 'changePercent', 'iexVolume', 'symbol', 'iexRealtimePrice', 'marketCap']]
        html += img[['url']]
        html += company[['CEO', 'website', 'description']]
        html = html.to_records()
        start = datetime(2020, 9, 12)
        today = datetime.today().date()
        historical_data_df = get_historical_data(search_term, start, today, output_format='pandas', token=IEX_API_TOKEN)
        historical_data_df['open'] = historical_data_df.open.astype(float)
        historical_data_df['high'] = historical_data_df.high.astype(float)
        historical_data_df['low'] = historical_data_df.low.astype(float)
        historical_data_df['close'] = historical_data_df.close.astype(float)
        data = historical_data_df.to_json()
        return render(request, "myapp/index.html", context={'html': html, 'api_json': data})

    return render(request, "myapp/index.html", context={})


# def chart(request):
#     search_term = ''
#     if 'search' in request.GET:
#         search_term = request.GET['search']
#         pd.set_option('display.max_columns', None)
#         search_term = request.GET['search']
#         start = datetime(2020, 9, 12)
#         today = datetime.utcnow().date()
#         historical_data_df = get_historical_data(search_term, start, today, output_format='pandas', token=IEX_API_TOKEN)
#         print(historical_data_df)
#         # Visualize the closing price history
#         plt.figure(figsize=(16, 8))
#         plt.title('Close Price History')
#         plt.plot(historical_data_df.index, historical_data_df['close'])
#         plt.xlabel('Change Over Time', fontsize=18)
#         plt.ylabel('Close Price USD ($)', fontsize=18)
#         plt.show()
#         # Second Visualization
#         historical_data_df['open'] = historical_data_df.open.astype(float)
#         historical_data_df['high'] = historical_data_df.high.astype(float)
#         historical_data_df['low'] = historical_data_df.low.astype(float)
#         historical_data_df['close'] = historical_data_df.close.astype(float)
#
#         figure = go.Figure(
#             data=[
#                 go.Candlestick(
#                     x=historical_data_df.index,
#                     open=historical_data_df['open'],
#                     high=historical_data_df['high'],
#                     low=historical_data_df['low'],
#                     close=historical_data_df['close'],
#                 )
#             ]
#         )
#         figure.update_layout(template='plotly_dark')
#         figure.update_layout(yaxis_title="USD Price ($)", xaxis_title='Date')
#         figure.show()
