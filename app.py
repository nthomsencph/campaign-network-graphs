from plotly.offline import iplot
import dash
import dash_core_components as dcc
import dash_html_components as html
from viz import create_cast_plot

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig = create_cast_plot()
# iplot(fig, filename = 'campaign')

app.layout = html.Div(children=[
    html.Div(children=[
        html.H2(children='Bridgelands'),
        html.H6("Relations between characters in the D&D campaign Bridgelands by Adnan Akçay."),
        html.Label(['Github repository: ', html.A('nthomsencph/campaign-network-graphs', href='https://github.com/nthomsencph/campaign-network-graphs')])]),
        
    dcc.Graph(
        id='scatter3d',
        figure=fig
    )
], 
style={
    'textAlign': "center",
    "margin": "0 auto",
    # 'align': "center",
    # 'width': "80&%",
    'color': "black",
    # 'display': 'inline-block', 
    'width': '100%',
    
    
})

if __name__ == '__main__':
    app.run_server() # the debug = True locally.
    