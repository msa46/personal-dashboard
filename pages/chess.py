import dash_mantine_components as dmc

from dash import Dash, html, register_page

register_page(__name__, path='/chess')

layout = html.Div(
    html.H1('Chess analysis')
)