import dash_mantine_components as dmc

from dash import Dash, html, register_page, dcc

from analysis.chessAnalysis import general_report, tactic_report

register_page(__name__, path='/chess')

def build_upper_panel():
    return dmc.Flex(
        id='upper-left',
        className='general comparison',
        children=[
            dmc.Card(children=[dcc.Graph(figure=general_report()),], 
                               withBorder=True,
                               shadow="sm",
                               radius="md",),
            dmc.Card(children=[dcc.Graph(figure=tactic_report())],
                               withBorder=True,
                               shadow="sm",
                               radius="md",)

        ],
        direction={'base': 'column', 'sm': 'row'},
        gap={'sm': 'lg'},
        justify={'sm': 'center'}
    )

layout = html.Div([
    html.H1('Chess analysis'),
    build_upper_panel()
])