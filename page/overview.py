import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

# import data
df_ = pd.read_csv("data/StudentFeedbackForm_May.csv")
print(df_.head(1))

std_df = df_[["gender", "have you heard/or learnt  about data science prior to this session?"]]
std_heard = std_df.groupby(['gender', 'have you heard/or learnt  about data science prior to this session?']).size().reset_index()
std_heard['percentage'] = std_df.groupby(['gender', 'have you heard/or learnt  about data science prior to this session?']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
std_heard.columns = ['gender', 'variables', 'counts', 'percentage']
# Bar Chart
fig_std_heard = px.bar(std_heard, x='gender', y='percentage', color='variables', 
    text=std_heard['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), 
    barmode="stack", color_discrete_map={"No":"lightpink", "Yes":"Lightgreen"}, height=400)

# percent of student learn new thing
std_lt_df = df_[["gender", "did you learn anything new? "]]
std_learnt = std_lt_df.groupby(['gender', 'did you learn anything new? ']).size().reset_index()
std_learnt['percentage'] = std_lt_df.groupby(['gender', 'did you learn anything new? ']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
std_learnt.columns = ['gender', 'variables', 'counts', 'percentage']
# Bar Chart
fig_std_learnt = px.bar(std_learnt, x='gender', y='percentage', color='variables', 
       text=std_learnt['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), 
       barmode="group", height=400, color_discrete_map={"No":"deeppink", "Yes":"Lightgreen"})

std_udt_df = df_[["gender", "was the presentation useful and/or simple to implement?"]]
std_udt_concep = std_udt_df.groupby(['gender', 'was the presentation useful and/or simple to implement?']).size().reset_index()
std_udt_concep['percentage'] = std_udt_df.groupby(['gender', 'was the presentation useful and/or simple to implement?']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
std_udt_concep.columns = ['gender', 'variables', 'counts', 'percentage']
# Bar Chart
fig_std_udt = px.bar(std_udt_concep, x='gender', y='percentage', color='variables', 
       text=std_udt_concep['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), 
       barmode="group", color_discrete_sequence=["deeppink","palegreen",], height=400)

# participation of student
std_part_df = df_[["gender", "was the training interactive enough?"]]
std_part = std_part_df.groupby(['gender', 'was the training interactive enough?']).size().reset_index()
std_part['percentage'] = std_part_df.groupby(['gender', 'was the training interactive enough?']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
std_part.columns = ['gender', 'variables', 'counts', 'percentage']
# Bar Chart
fig_std_part = px.bar(std_part, x='gender', y='percentage', color='variables', 
       text=std_part['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), 
       barmode="stack", height=400, color_discrete_sequence=["lightpink","palegreen",])

# Percentage of students who would like further training
std_further_df = df_[["gender", "would you like to have advance training sessions?"]]
std_further = std_further_df.groupby(['gender', 'would you like to have advance training sessions?']).size().reset_index()
std_further['percentage'] = std_further_df.groupby(['gender', 'would you like to have advance training sessions?']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
std_further.columns = ['gender', 'variables', 'counts', 'percentage']
# Bar Chart
fig_std_further = px.bar(std_further, x='gender', y='percentage', color='variables', 
       text=std_further['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), 
       barmode="group", color_discrete_map={"No":"deeppink", "Yes":"Lightgreen"}, height=400)

# Percentage of Students who feel comfortable choosing a career in technology
std_choose_df = df_[["gender", "after this training, do you feel comfortable choosing a career in technology?"]]
std_choose = std_choose_df.groupby(['gender', 'after this training, do you feel comfortable choosing a career in technology?']).size().reset_index()
std_choose['percentage'] = std_choose_df.groupby(['gender', 'after this training, do you feel comfortable choosing a career in technology?']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
std_choose.columns = ['gender', 'variables', 'counts', 'percentage']
# Bar Chart
fig_std_choose = px.bar(std_choose, x='gender', y='percentage', color='variables', 
       text=std_choose['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), 
       barmode="stack", height=400, color_discrete_sequence=["lightpink","palegreen",])

# Quality training rating among students
std_rate_training = df_["how would you rate the quality of the training?"].value_counts()
fig_std_rate_training = px.pie(df_, values=std_rate_training, names=std_rate_training.index, 
                              hole=0.2, color=std_rate_training.index, color_discrete_map={'Very Good':'lightblue',
                                 'Moderate':'cyan',
                                 'Good':'yellow',
                                 'Excellent':'darkblue'}, height=400)
fig_std_rate_training.update_traces(textinfo='percent+label',)

# Quality of the trainer
std_rate_trainer = df_["how would you rate the quality of the trainer?"].value_counts()
fig_std_rate_trainer = px.pie(df_, values=std_rate_trainer, names=std_rate_trainer.index, hole=0.2)
fig_std_rate_trainer.update_traces(textinfo='percent+label')

# Recommend training to friends and schoolmates
std_recommend_df = df_[["gender", "would you recommend the training to friends and schoolmates?"]]
std_recommend = std_recommend_df.groupby(['gender', 'would you recommend the training to friends and schoolmates?']).size().reset_index()
std_recommend['percentage'] = std_recommend_df.groupby(['gender', 'would you recommend the training to friends and schoolmates?']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
std_recommend.columns = ['gender', 'variables', 'counts', 'percentage']
# Bar Chart
fig_std_recommend = px.bar(std_recommend, x='gender', y='percentage', color='variables', 
       text=std_recommend['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), 
       barmode="group", height=400, color_discrete_sequence=["deeppink","palegreen",])

# Overall Training Performance Score
train_ = df_.groupby("gender")["training_performance_score"].mean().reset_index()
fig_train = px.bar(train_, x='gender', y='training_performance_score', color='training_performance_score', 
       text=train_['training_performance_score'].apply(lambda x: '{0:1.2f}%'.format(x)), 
       height=400, color_discrete_sequence=["deeppink","palegreen",])

layout = dbc.Container([

    html.Div(
        [
            dbc.Row(
                dbc.Col(
                    html.H2("STUDENTS FEEDBACK ANALYSIS"), 
                    width={"size": 6, "offset": 3},
                )
            ),
            dbc.Row(
                [
                    dbc.Col([
                        html.Li("Percentage of students who heard/never heard about data science before."),
                        dcc.Graph(id="fig1", figure=fig_std_heard)
                    ],
                        width={"size": 4,},
                    ),
                    dbc.Col([
                        html.Li("Percentage of students who learnt/didn’t learn something new from training"),
                        dcc.Graph(id="fig2", figure=fig_std_learnt)
                    ],
                        width={"size": 4,},
                    ),
                    dbc.Col([
                        html.Li("Was the training simple enough for students to understand concepts?"),
                        dcc.Graph(id="fig3", figure=fig_std_udt)
                    ],
                        width={"size": 4,},
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
                        width={"size": 4, },
                    ),
                    dbc.Col([
                        html.Li("Percentage of students who would like further training"),
                        dcc.Graph(id="fig5", figure=fig_std_further)
                    ],
                        width={"size": 4,},
                    ),
                    dbc.Col([
                        html.Li("Percentage of Students who feel comfortable choosing a career in technology"),
                        dcc.Graph(id="fig6", figure=fig_std_choose)
                    ],
                        width={"size": 4,},
                    ),
                ]
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col([
                        html.Li("How is the Quality of the training rated?"),
                        dcc.Graph(id="fig7", figure=fig_std_rate_training)
                    ],
                        width={"size": 4, },
                    ),
                    dbc.Col([
                        html.Li("Percentage of students who would recommend training to friends and schoolmates"),
                        dcc.Graph(id="fig8", figure=fig_std_recommend)
                    ],
                        width={"size": 4,},
                    ),
                    dbc.Col([
                    html.Li("Overall Training Performance Score"),
                    dcc.Graph(id="fig9", figure=fig_train)
                    ],
                        width={"size": 4,},
                    ),
                ]
            ),
        ]
    )

])