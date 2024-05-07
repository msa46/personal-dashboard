import dash_mantine_components as dmc
from dash import html, dcc, page_container, page_registry

from app import app


app.layout = dmc.MantineProvider(
    forceColorScheme='dark',
    children=[
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        dmc.NavLink(label=f"{page['name']} - {page['path']}", 
                    href=page["relative_path"],
                    active=True
                    )
         for page in page_registry.values()
    ]),
    page_container
])

if __name__ == '__main__':
    app.run(debug=True)