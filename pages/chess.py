import dash_mantine_components as dmc

from dash import Dash, html, register_page, dcc

from analysis.chessAnalysis import general_report

register_page(__name__, path='/chess')

def build_upper_left_panel():
    return html.Div(
        id='upper-left',
        className='general comparison',
        children=[
            dcc.Graph(figure=general_report())
        ]
    )

layout = html.Div([
    html.H1('Chess analysis'),
    build_upper_left_panel()
])