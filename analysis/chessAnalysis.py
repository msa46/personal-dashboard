import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv('data/chess_games.csv')

# Define the colors for the dark mode palette
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


    fig = px.pie(final_df, values='count_percent', names='opening_shorten')

    fig.update_traces(text=final_df['CustomText'], 
                      textinfo='text', 
                      textfont=dict(color='white'),
                      marker=dict(colors=dark_mode_palette)
                      )
    fig.update_layout(
        # width=900, 
        height=500,  
        plot_bgcolor='rgb(22,26,29)',
        paper_bgcolor='rgb(22,26,29)',
        margin=dict(t=0, b=0, l=0, r=20),  # Reduce whitespace by adjusting margins (top, bottom, left, right)
        legend_font_color='white'
    )

    return fig