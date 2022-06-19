from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from page import overview, sch_level
from app import app, server

DSTI_LOGO = "data:image/png;base64,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"

navbar = dbc.Navbar(
    children=[
        dbc.Container(
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=DSTI_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("CAREERS IN TECH", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),





        ),
        dbc.NavItem(dbc.NavLink("Overall", href="/", style={"color": "white"}) ),
        dbc.NavItem(dbc.NavLink("School_Level", href="/school_level",style={"color": "white"}) ),
    ],

    color="dark",
    dark=True,


)


# app.layout = dbc.Container(row, fluid=False)

content = html.Div(id="page-content", children=[],)


app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    content])


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')]
              )
def render_page_content(pathname):
    if pathname == '/':
        return overview.layout
    elif pathname == '/school_level':
        return sch_level.layout
    # If the user tries to reach a different page, return a 404 message
    else:
        return html.Div(
            dbc.Container(
                [
                    html.H1("404: Not found", className="text-danger"),
                    html.Hr(),
                    html.P(
                        f"The pathname {pathname} was not recognised..."),
                ],
                fluid=True,
                className="py-3",
            ),
            className="p-3 bg-light rounded-3",
        )


if __name__ == "__main__":
    app.run_server(debug=True)
