import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv('data/chess_games.csv')

dark_mode_palette = [
    '#1f77b4',  # Muted Blue
    '#2ca02c',  # Cooked Asparagus Green
    '#d62728',  # Brick Red
    '#9467bd',  # Muted Purple
    '#8c564b',  # Chestnut Brown
    '#e377c2',  # Raspberry Yogurt Pink
    '#7f7f7f',  # Middle Gray
    '#bcbd22',  # Curry Yellow-Green
    '#17becf',  # Blue-Teal
    '#393b79',   # Dark Blue
    '#5a4f7c',  # Lighter Dark Purple
]

def shorten_name(row):
    splited_name = row['opening_name'].split(' ')
    if len(splited_name) >= 2:
        second_part = splited_name[1]
        if ':' in second_part:
            second_part = second_part[:-1]
        return splited_name[0] + " " +  second_part
    else:
        return row['opening_name']
    
df['opening_shorten'] = df.apply(shorten_name, axis=1)

def general_report():
    grouped = df.groupby('opening_shorten').size().reset_index(name='count')
    grouped_sorted = grouped.sort_values(by='count', ascending=False)

    total = grouped_sorted['count'].sum()

    grouped_sorted['count_percent'] = (grouped_sorted['count'] / total) * 100

    top = grouped_sorted.head(10)

    others= pd.DataFrame(data = {
        'opening_shorten': ['others'],
        'count_percent': [grouped_sorted['count_percent'][10:].sum()]
    })

    final_df = pd.concat([top, others])
    final_df['CustomText'] = final_df.apply(lambda x: f"{x['opening_shorten']}: {x['count_percent']:.2f}%" if x['count_percent'] >= 1 else None, axis=1)


    fig = px.pie(final_df, values='count_percent', names='opening_shorten', title='Tactics')

    fig.update_traces(text=final_df['CustomText'], 
                      textinfo='text', 
                      textfont=dict(color='white'),
                      marker=dict(colors=dark_mode_palette)
                      )
    fig.update_layout(
        height=650,
        plot_bgcolor='rgb(22,26,29)',
        paper_bgcolor='rgb(22,26,29)',
        margin=dict(t=50, b=15, l=10, r=20),  
        legend_font_color='white',
        title_font_color='white',
    )

    return fig

def tactic_report():

    tactic_df = df.assign(
    opening_side = lambda x: np.where(x['opening_name'].str.contains('Defense|King\'s Indian'), 'black', 'white'),
    tactic_worked = lambda x: np.where((x['opening_side'] == x['winner']), True, False)
    )
    tactic_df = tactic_df.groupby('tactic_worked').size().reset_index(name='tactic_sum')
    tactic_df['tactic_worked_str'] = tactic_df['tactic_worked'].replace({True: 'Worked', False: 'Did Not Work'})


    fig = px.pie(tactic_df, values='tactic_sum', names='tactic_worked_str', color='tactic_worked_str',
                color_discrete_map={
                    'Did Not Work': '#9467bd',
                    'Worked': '#1f77b4'
                },
                title='Used tactic result'
                )
                

    fig.update_layout(
        height=650,
        plot_bgcolor='rgb(22,26,29)',
        paper_bgcolor='rgb(22,26,29)',        
        margin=dict(t=50, b=15, l=10, r=20),  
        legend_font_color='white',
        title_font_color='white',

    )

    return fig

def strategy_report(selected_strategy):
    specific_df = df.assign(
        opening_side = lambda x: np.where(x['opening_name'].str.contains('Defense|King\'s Indian'), 'black', 'white'),
        tactic_worked = lambda x: np.where((x['opening_side'] == x['winner']), True, False)
    )
    specific_df = specific_df[df.opening_shorten == selected_strategy]
    grouped_specific_df =  specific_df.groupby(['opening_name', 'tactic_worked']).size().reset_index(name='count')
    grouped_specific_df = grouped_specific_df.sort_values(by='count', ascending=False)

    total_count = grouped_specific_df.groupby('opening_name')['count'].sum()
    grouped_specific_df = grouped_specific_df.merge(total_count, on='opening_name', suffixes=('', '_total'))
    grouped_specific_df = grouped_specific_df.sort_values(by='count_total', ascending=False)
    grouped_specific_df['tactic_worked_str'] = grouped_specific_df['tactic_worked'].replace({True: 'Worked', False: 'Did Not Work'})

    custom_colors = ['#1f77b4', '#9467bd']

    

    fig = px.bar(grouped_specific_df.head(12), 
                 x='opening_name', 
                 y='count', 
                 color='tactic_worked_str', 
                 color_discrete_sequence=custom_colors)

    fig.update_layout(
        plot_bgcolor='rgb(22,26,29)',
        paper_bgcolor='rgb(22,26,29)',        
        margin=dict(t=50, b=15, l=10, r=20),  
        legend_font_color='white',
        title_font_color='white',
        legend_title_text='Tactic result'
        

    )
    fig.update_xaxes(color='white', title_text= 'Opening name')
    fig.update_yaxes(color='white') 
    return fig

def winrate_to_total_report():
    grouped_tactic = df.assign(
        opening_side = lambda x: np.where(x['opening_name'].str.contains('Defense|King\'s Indian'), 'black', 'white'),
        tactic_worked = lambda x: np.where((x['opening_side'] == x['winner']), True, False)
    )
    grouped_tactic = grouped_tactic.groupby(['opening_shorten','tactic_worked']).size().reset_index(name='per_tactic_result')

    total_count = grouped_tactic.groupby('opening_shorten')['per_tactic_result'].sum()

    grouped_tactic = grouped_tactic.merge(total_count, on='opening_shorten', suffixes=('', '_total'))
    grouped_tactic['percentage'] =(grouped_tactic['per_tactic_result'] / grouped_tactic['per_tactic_result_total']) * 100 

    only_wins_df = grouped_tactic[grouped_tactic['tactic_worked'] == True]
    only_wins_df = only_wins_df.sort_values(by='percentage')
    mean = only_wins_df['percentage'].mean()
    std = only_wins_df['percentage'].std()
    x_values = np.linspace(mean - 4*std, mean + 4*std, 400)
    y_values = np.exp(-(x_values - mean)**2 / (2 * std**2)) / (std * np.sqrt(2 * np.pi))

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=only_wins_df['percentage'], y=only_wins_df['per_tactic_result_total'], histnorm='probability density', name='total played vs winning%'))
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name='Normal Distribution'))


    fig.update_layout(
        height=500,
        title='Distribution of Winning Percentages by Total Tactics Played',
        plot_bgcolor='rgb(22,26,29)',
        paper_bgcolor='rgb(22,26,29)',        
        margin=dict(t=50, b=15, l=10, r=20),  
        legend_font_color='white',
        title_font_color='white',
    )

    fig.update_xaxes(color='white', title_text= 'Win percent')
    fig.update_yaxes(color='white', title='ُTotal players') 

    return fig