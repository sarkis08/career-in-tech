import dash_bootstrap_components as dbc
from dash import html, dcc
import dash
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px

from app import app

# import data
df_ = pd.read_csv("data/StudentFeedbackForm_May.csv")

layout = dbc.Container([

    html.Div([

        html.H2("SCHOOL LEVEL FEEDBACK ANALYSIS",
                style={"textAlign": "center"}),
        dbc.Row([
            html.H3("Filtering"),

            dbc.Col([
                html.Pre(children="School Name", style={"fontSize": "100%"}),
                dcc.Dropdown(
                    id='schname-dpdn',
                    placeholder="Select School",
                    value=None,
                    clearable=True,
                    persistence=True,
                    persistence_type='session',
                    options=[{'label': x, 'value': x}
                             for x in sorted(df_.schoolname.unique())]
                )
            ], width={"size": 4}),

            dbc.Col([
                html.Pre(children="Class", style={"fontSize": "100%"}),
                dcc.Dropdown(
                    id='class-dpdn',
                    placeholder="Select Class",
                    clearable=True,
                    persistence=True,
                    multi=True,
                    persistence_type='session',
                    value=[],
                    options=[],

                )
            ], width={"size": 4}),
            dbc.Col([
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                f"Overall Training Performance Score"),
                            dbc.CardBody(
                                [
                                    html.H4(df_["training_performance_score"].mean().round(2),
                                            className="card-title",
                                            style={"textAlign": "center"}),
                                ]
                            ),
                        ],
                        color="success",
                        outline=True,

                    )],
                    width={'size': 4, }),
        ], ),  # end of row
        html.Br(),
        html.Br(),
        dbc.Row(
            [

                html.H5("Did students learn anything from training?"),

                dbc.Col([
                        html.Li(
                            "Percentage of students who heard/never heard about data science before."),
                        html.Div(id='graph-container1', children=[],),

                        ],
                        width={"size": 6, },
                        ),
                dbc.Col([
                        html.Li(
                            "Percentage of students who learnt/didn’t learn something new from trainin"),
                        html.Div(id='graph-container2', children=[],),
                        ],
                        width={"size": 6, },
                        ),
            ],),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col([
                        html.Li(
                            "Was the training simple enough for students to understand concepts?"),
                        html.Div(id='graph-container3', children=[],),

                        ],
                        width={"size": 4, },
                        ),
                dbc.Col([
                        html.Li(
                            "Was the training interactive and involved a lot of participation by students?"),
                        html.Div(id='graph-container4', children=[],),
                        ],
                        width={"size": 4, },
                        ),
                dbc.Col([
                    html.Li(
                        "Percentage of students who would recommend training to friends and schoolmates"),
                    html.Div(id='graph-container5', children=[],),

                ],
                    width={"size": 4, },
                ),
            ],),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                html.H5(
                    "Do students prefer further training or feel comfortable choosing a career in technology?"),
                dbc.Col([
                        html.Li(
                            "Percentage of students who would like further training"),
                        html.Div(id='graph-container6', children=[],),

                        ],
                        width={"size": 6, },
                        ),
                dbc.Col([
                        html.Li(
                            "Percentage of Students who feel comfortable choosing a career in technology"),
                        html.Div(id='graph-container7', children=[],),
                        ],
                        width={"size": 6, },
                        ),
            ],),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [

                dbc.Col([
                        html.Li(
                            "How is the Quality of the training rated?"),
                        html.Div(id='graph-container8', children=[],),
                        ],
                        width={"size": 6, "offset": 3 },
                        ),
            ],),
    ]),
    html.Div()
])

# Populate classes dropdown with options and values


@app.callback(
    [Output(component_id='class-dpdn', component_property='options'),
     Output(component_id='class-dpdn', component_property='value'), ],
    [Input(component_id='schname-dpdn', component_property='value'), ],
)
def set_classes_options(chosen_schname):
    df = df_[df_.schoolname == chosen_schname]
    class_names = [{'label': s, 'value': s}
                   for s in sorted(df['class'].unique())]
    val_name = [x['value'] for x in class_names]
    return class_names, val_name

# Create graph component and populate with scatter plot


@app.callback(
    [Output('graph-container1', 'children'),
     Output('graph-container2', 'children'),
     Output('graph-container3', 'children'),
     Output('graph-container4', 'children'),
     Output('graph-container5', 'children'),
     Output('graph-container6', 'children'),
     Output('graph-container7', 'children'),
     Output('graph-container8', 'children'), ],
    Input('schname-dpdn', 'value'),
    Input('class-dpdn', 'value'),
    prevent_initial_call=True
)
def update_grpah(selected_schname, selected_class):
    dff = df_.copy()
    if len(selected_class) == 0:
        return dash.no_update
    else:
        
        sdf = dff[(dff["schoolname"] == selected_schname) & (dff['class'].isin(selected_class))]
        # print(sdf.head())
        std_df = sdf[[
            "gender", "have you heard/or learnt  about data science prior to this session?"]]
        std_heard = std_df.groupby(
            ['gender', 'have you heard/or learnt  about data science prior to this session?']).size().reset_index()
        std_heard['percentage'] = std_df.groupby(['gender', 'have you heard/or learnt  about data science prior to this session?']).size(
        ).groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
        std_heard.columns = ['gender', 'variables', 'counts', 'percentage']

        fig_sch_hd = px.bar(std_heard, x='gender', y='percentage', color='variables',
                            text=std_heard['percentage'].apply(
                                lambda x: '{0:1.2f}%'.format(x)),
                            barmode="stack", color_discrete_map={"No": "lightpink", "Yes": "Lightgreen"}, height=400)

        # percent of student learn new thing
        std_lt_df = sdf[["gender", "did you learn anything new? "]]
        std_learnt = std_lt_df.groupby(
            ['gender', 'did you learn anything new? ']).size().reset_index()
        std_learnt['percentage'] = std_lt_df.groupby(['gender', 'did you learn anything new? ']).size(
        ).groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
        std_learnt.columns = ['gender', 'variables', 'counts', 'percentage']
        # Bar Chart
        fig_std_learnt = px.bar(std_learnt, x='gender', y='percentage', color='variables',
                                text=std_learnt['percentage'].apply(
                                    lambda x: '{0:1.2f}%'.format(x)),
                                barmode="group", height=400, color_discrete_map={"No": "deeppink", "Yes": "Lightgreen"})

        std_udt_df = sdf[[
            "gender", "was the presentation useful and/or simple to implement?"]]
        std_udt_concep = std_udt_df.groupby(
            ['gender', 'was the presentation useful and/or simple to implement?']).size().reset_index()
        std_udt_concep['percentage'] = std_udt_df.groupby(
            ['gender', 'was the presentation useful and/or simple to implement?']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
        std_udt_concep.columns = [
            'gender', 'variables', 'counts', 'percentage']
        # Bar Chart
        fig_std_udt = px.bar(std_udt_concep, x='gender', y='percentage', color='variables',
                             text=std_udt_concep['percentage'].apply(
                                 lambda x: '{0:1.2f}%'.format(x)),
                             barmode="group", color_discrete_sequence=["deeppink", "palegreen", ], height=400)

        # participation of student
        std_part_df = sdf[["gender", "was the training interactive enough?"]]
        std_part = std_part_df.groupby(
            ['gender', 'was the training interactive enough?']).size().reset_index()
        std_part['percentage'] = std_part_df.groupby(['gender', 'was the training interactive enough?']).size(
        ).groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
        std_part.columns = ['gender', 'variables', 'counts', 'percentage']
        # Bar Chart
        fig_std_part = px.bar(std_part, x='gender', y='percentage', color='variables',
                              text=std_part['percentage'].apply(
                                  lambda x: '{0:1.2f}%'.format(x)),
                              barmode="stack", height=400, color_discrete_sequence=["lightpink", "palegreen", ])

        # Recommend training to friends and schoolmates
        std_recommend_df = sdf[[
            "gender", "would you recommend the training to friends and schoolmates?"]]
        std_recommend = std_recommend_df.groupby(
            ['gender', 'would you recommend the training to friends and schoolmates?']).size().reset_index()
        std_recommend['percentage'] = std_recommend_df.groupby(['gender', 'would you recommend the training to friends and schoolmates?']).size(
        ).groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
        std_recommend.columns = ['gender', 'variables', 'counts', 'percentage']
        # Bar Chart
        fig_std_recommend = px.bar(std_recommend, x='gender', y='percentage', color='variables',
                                   text=std_recommend['percentage'].apply(
                                       lambda x: '{0:1.2f}%'.format(x)),
                                   barmode="group", height=400, color_discrete_sequence=["deeppink", "palegreen", ])

        # Percentage of students who would like further training
        std_further_df = sdf[[
            "gender", "would you like to have advance training sessions?"]]
        std_further = std_further_df.groupby(
            ['gender', 'would you like to have advance training sessions?']).size().reset_index()
        std_further['percentage'] = std_further_df.groupby(['gender', 'would you like to have advance training sessions?']).size(
        ).groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
        std_further.columns = ['gender', 'variables', 'counts', 'percentage']
        # Bar Chart
        fig_std_further = px.bar(std_further, x='gender', y='percentage', color='variables',
                                 text=std_further['percentage'].apply(
                                     lambda x: '{0:1.2f}%'.format(x)),
                                 barmode="group", color_discrete_map={"No": "deeppink", "Yes": "Lightgreen"}, height=400)

        # Percentage of Students who feel comfortable choosing a career in technology
        std_choose_df = sdf[[
            "gender", "after this training, do you feel comfortable choosing a career in technology?"]]
        std_choose = std_choose_df.groupby(
            ['gender', 'after this training, do you feel comfortable choosing a career in technology?']).size().reset_index()
        std_choose['percentage'] = std_choose_df.groupby(['gender', 'after this training, do you feel comfortable choosing a career in technology?']).size(
        ).groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
        std_choose.columns = ['gender', 'variables', 'counts', 'percentage']
        # Bar Chart
        fig_std_choose = px.bar(std_choose, x='gender', y='percentage', color='variables',
                                text=std_choose['percentage'].apply(
                                    lambda x: '{0:1.2f}%'.format(x)),
                                barmode="group", height=400, color_discrete_sequence=["lightpink", "palegreen", ])

        # Quality training rating among students
        std_rate_training = sdf["how would you rate the quality of the training?"].value_counts(
        )
        fig_std_rate_training = px.pie(sdf, values=std_rate_training, names=std_rate_training.index,
                                       hole=0.2, color=std_rate_training.index, 
                                       color_discrete_map={'Very Good': 'lightblue','Moderate': 'cyan',
                                                'Good': 'yellow','Excellent': 'darkblue'}, height=400)
        fig_std_rate_training.update_traces(textinfo='percent+label',)
    
    return [dcc.Graph(id="fig1", figure=fig_sch_hd,), dcc.Graph(id="fig2", figure=fig_std_learnt,),
            dcc.Graph(id="fig3", figure=fig_std_udt,), dcc.Graph(
                id="fig4", figure=fig_std_part,),
            dcc.Graph(id="fig5", figure=fig_std_recommend,), dcc.Graph(
                id="fig6", figure=fig_std_further,),
            dcc.Graph(id="fig7", figure=fig_std_choose,), dcc.Graph(id="fig8", figure=fig_std_rate_training,),]
