from dash.dependencies import Input, Output

from app import app
from analysis.chessAnalysis import strategy_report
@app.callback(
    Output('strategy-graph', 'figure'),
    [Input('strategy-dropdown', 'value')]
)
def update_strategy_graph(selected_strategy):

    return strategy_report(selected_strategy)