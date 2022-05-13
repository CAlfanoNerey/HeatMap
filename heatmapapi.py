#!/usr/bin/env python3
from http.client import responses
from random import randint
import pandas as pd
import numpy as np

import plotly.express as px


import dash
import dash_core_components as dcc
import dash_html_components as html

import json
import requests
from requests.auth import HTTPBasicAuth
app = dash.Dash()

def serve_layout():
    app = dash.Dash()

    response = requests.get('https://api.coingecko.com/api/v3/exchange_rates')
    page = json.loads(response.content)
    currency = []
    value = []
    duration = []

    count = 0

    for crypto in page['rates']:
        
        # Get BTC-to-Currency exchange rates
        currency.append(crypto)
        value.append(page['rates'][crypto]['value'])
        duration.append(randint(100,5000))

        if(count == 10):
            break
        count += 1
        


    df = pd.DataFrame(
        dict(currency=currency, value=value, duration=duration)
    )
    print(df)
    df["all"] = "all"
    fig = px.treemap(df,
                    path=["currency"],
                    values='value',color='duration', color_continuous_scale=[[0, '#0066ff'],[0.5, '#ffff99'], [1, '#ff0000']],)


    fig.update_layout(
        uniformtext=dict(minsize=20, mode='show'),
        # margin = dict(t=100, l=25, r=25, b=0)
    )
    
    # fig.show()

    # fig.show()

    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])
    return app.layout
    
app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)  # Turn off reloader if inside Jupyter