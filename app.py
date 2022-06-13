from tkinter.ttk import Style
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server
# import data
df_ = pd.read_csv("data/StudentFeedbackForm_May.csv")
print(df_.head(1))

# percent of student learn or heard
std_hd = df_["have you heard/or learnt  about data science prior to this session?"].value_counts()
fig_std_hd = px.pie(df_, values=std_hd, names=std_hd.index, hole=0.2)
fig_std_hd.update_traces(textinfo='percent+label')

# percent of student learn new thing
std_lt = df_["did you learn anything new? "].value_counts()
fig_std_lt = px.pie(df_, values=std_lt, names=std_lt.index, hole=0.2)
fig_std_lt.update_traces(textinfo='percent+label')

std_udt = df_["was the presentation useful and/or simple to implement?"].value_counts()
fig_std_udt = px.pie(df_, values=std_udt, names=std_udt.index, hole=0.2)
fig_std_udt.update_traces(textinfo='percent+label')

# participation of student
std_part = df_["was the training interactive enough?"].value_counts()
fig_std_part = px.pie(df_, values=std_part, names=std_part.index, hole=0.2)
fig_std_part.update_traces(textinfo='percent+label')

# Percentage of students who would like further training
std_further = df_["would you like to have advance training sessions?"].value_counts()
fig_std_further = px.pie(df_, values=std_further, names=std_further.index, hole=0.2)
fig_std_further.update_traces(textinfo='percent+label')

# Percentage of Students who feel comfortable choosing a career in technology
std_choose = df_["after this training, do you feel comfortable choosing a career in technology?"].value_counts()
fig_std_choose = px.pie(df_, values=std_choose, names=std_choose.index, hole=0.2)
fig_std_choose.update_traces(textinfo='percent+label')

# Quality training rating among students
std_qty_rate = df_["how would you rate the quality of the training?"].value_counts()
fig_std_qty_rate = px.pie(df_, values=std_qty_rate, names=std_qty_rate.index, hole=0.2)
fig_std_qty_rate.update_traces(textinfo='percent+label')

# Quality of the trainer
std_rate_trainer = df_["how would you rate the quality of the trainer?"].value_counts()
fig_std_rate_trainer = px.pie(df_, values=std_rate_trainer, names=std_rate_trainer.index, hole=0.2)
fig_std_rate_trainer.update_traces(textinfo='percent+label')

row = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.H1("CAREERS IN TECH ANALYSIS: DATA SCIENCE INTRO"),
                width={"size": 8, "offset": 2},
            )
        ),
        dbc.Row(
            [
                dbc.Col([
                    html.Li("Percentage of students who heard/never heard about data science before."),
                    dcc.Graph(id="fig1", figure=fig_std_hd)
                ],
                    width={"size": 3, "order": 1, "offset": 1},
                ),
                dbc.Col([
                    html.Li("Percentage of students who learnt/didn’t learn something new from training"),
                    dcc.Graph(id="fig2", figure=fig_std_lt)
                ],
                    width={"size": 3, "order": 2, "offset": 1},
                ),
                dbc.Col([
                    html.Li("Was the training simple enough for students to understand concepts?"),
                    dcc.Graph(id="fig3", figure=fig_std_udt)
                ],
                    width={"size": 3, "order": "last", "offset":1},
                ),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col([
                    html.Li("Was the training interactive and involved a lot of participation by students?"),
                    dcc.Graph(id="fig4", figure=fig_std_part)
                ],
                    width={"size": 3, "order": 1, "offset": 1},
                ),
                dbc.Col([
                    html.Li("Percentage of students who would like further training"),
                    dcc.Graph(id="fig5", figure=fig_std_further)
                ],
                    width={"size": 3, "order": 2, "offset": 1},
                ),
                dbc.Col([
                    html.Li("Percentage of Students who feel comfortable choosing a career in technology"),
                    dcc.Graph(id="fig6", figure=fig_std_choose)
                ],
                    width={"size": 3, "order": "last", "offset":1},
                ),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col([
                    html.Li("How is the Quality of the trainer rated?"),
                    dcc.Graph(id="fig7", figure=fig_std_rate_trainer)
                ],
                    width={"size": 4, "order": 1, "offset": 1},
                ),
                dbc.Col([
                    html.Li("How is the Quality of the training rated?"),
                    dcc.Graph(id="fig8", figure=fig_std_qty_rate)
                ],
                    width={"size": 4, "order": 2, "offset": 1},
                ),
            ]
        ),
    ]
)

app.layout = dbc.Container(row, fluid=True)


if __name__ == "__main__":
    app.run_server(debug=True)
