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

def build_middle_panel():
    strategy_list = ["Sicilian Defense", "French Defense", "Queen's Pawn", "Italian Game",
                     "King's Pawn", "Queen's Gambit", "Ruy Lopez", "English Opening",
                     "Scandinavian Defense", "Philidor Defense"
                     ]
    return dmc.Flex(
        children=[
            dmc.Flex(
                children=[
                dmc.Select(
                    data=[{'label': strategy, 'value': strategy} for strategy in strategy_list],
                    value='Sicilian Defense',
                    id='strategy-dropdown'
                ),
                dmc.Card(children=[dcc.Graph(id='strategy-graph')],
                                withBorder=True,
                                shadow="sm",
                                radius="md",)
            ],
            direction='column',
            gap='sm'),],
            direction='column',
            )
            
    
layout = html.Div([
    html.H1('Chess analysis'),
    dmc.Flex(children=[
    build_upper_panel(),
    build_middle_panel(),
    ],
    direction='column',
    gap='sm',)
])
