import pandas as pd
import numpy as np
import sys
import textwrap
import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objs as go

# taking the user input as a string
user_input = sys.argv[0]

# loading in the tweet dataset
df_earthquake = pd.read_csv('./final_labeled_earthquake.csv')
df_wildfire = pd.read_csv('./final_labeled_wildfire.csv')
df_hurricane = pd.read_csv('./final_labeled_hurricane.csv')

# create a function to create a list of 1s and 0s
def strict_matches_df(user_input, user_event):
    df = None

    if user_event == "hurricane":
        df = df_hurricane
    elif user_event == "wildfire":
        df = df_wildfire
    elif user_event == "earthquake":
        df = df_earthquake
    elif user_event == "all":
        df = pd.concat([df_earthquake, df_wildfire, df_hurricane])

    matches = []
    # split the entered keywords by comma
    keywords = user_input.split(',')
    # create an empty list to store keywords
    keyword_list = []
    for i in range(len(keywords)):
        # remove white space
        keywords[i] = keywords[i].strip()
        print(keywords[i])
        # append it to keyword_list
        keyword_list.append(keywords[i])

    # resetting the df to be just latitude longitude and clean text
    df = df[['lat', 'long', 'text_clean']]
    df['text_clean'] = df["text_clean"].apply(lambda t: "<br>".join(textwrap.wrap(t)))

    # filtering the dataframe to be include ONLY tweets that include ALL of the keywords
    if len(keyword_list) == 1:
        df = df[df['text_clean'].str.contains(keyword_list[0])]

    if len(keyword_list) == 2:
        df = df[df['text_clean'].str.contains(keyword_list[0]) & df['text_clean'].str.contains(keyword_list[1])]

    elif len(keyword_list) == 3:
        df = df[df['text_clean'].str.contains(keyword_list[0]) & df['text_clean'].str.contains(keyword_list[1]) & df['text_clean'].str.contains(keyword_list[2])]

    elif len(keyword_list) == 4:
        df = df[df['text_clean'].str.contains(keyword_list[0]) & df['text_clean'].str.contains(keyword_list[1]) & df['text_clean'].str.contains(keyword_list[2])
        & df['text_clean'].str.contains(keyword_list[3])]

    elif len(keyword_list) == 5:
        df = df[df['text_clean'].str.contains(keyword_list[0]) & df['text_clean'].str.contains(keyword_list[1]) & df['text_clean'].str.contains(keyword_list[2])
        & df['text_clean'].str.contains(keyword_list[3]) & df['text_clean'].str.contains(keyword_list[4])]

    elif len(keyword_list) == 6:
        df = df[df['text_clean'].str.contains(keyword_list[0]) & df['text_clean'].str.contains(keyword_list[1]) & df['text_clean'].str.contains(keyword_list[2])
        & df['text_clean'].str.contains(keyword_list[3]) & df['text_clean'].str.contains(keyword_list[4]) & df['text_clean'].str.contains(keyword_list[5])]
    return df

def loose_matches_df(user_input, user_event):
    df = None

    if user_event == "hurricane":
        df = df_hurricane
    elif user_event == "wildfire":
        df = df_wildfire
    elif user_event == "earthquake":
        df = df_earthquake
    elif user_event == "all":
        df = pd.concat([df_earthquake, df_wildfire])

    matches = []
    # split the entered keywords by comma
    keywords = user_input.split(',')
    # create an empty list to store keywords
    keyword_list = []
    for i in range(len(keywords)):
        # remove white space
        keywords[i] = keywords[i].strip()
        print(keywords[i])
        # append it to keyword_list
        keyword_list.append(keywords[i])
    # resetting the df to be just latitude longitude and clean text
    df = df[['lat', 'long', 'text_clean']]
    df['text_clean'] = df["text_clean"].apply(lambda t: "<br>".join(textwrap.wrap(t)))

    # filtering the dataframe to be include tweets that include ANY of the keywords
    if len(keyword_list) == 1:
        df = df[df['text_clean'].str.contains(keyword_list[0])]

    if len(keyword_list) == 2:
        df = df[df['text_clean'].str.contains(keyword_list[0]) | df['text_clean'].str.contains(keyword_list[1])]

    elif len(keyword_list) == 3:
        df = df[df['text_clean'].str.contains(keyword_list[0]) | df['text_clean'].str.contains(keyword_list[1]) | df['text_clean'].str.contains(keyword_list[2])]

    elif len(keyword_list) == 4:
        df = df[df['text_clean'].str.contains(keyword_list[0]) | df['text_clean'].str.contains(keyword_list[1]) | df['text_clean'].str.contains(keyword_list[2])
        | df['text_clean'].str.contains(keyword_list[3])]

    elif len(keyword_list) == 5:
        df = df[df['text_clean'].str.contains(keyword_list[0]) | df['text_clean'].str.contains(keyword_list[1]) | df['text_clean'].str.contains(keyword_list[2])
        | df['text_clean'].str.contains(keyword_list[3]) | df['text_clean'].str.contains(keyword_list[4])]

    elif len(keyword_list) == 6:
        df = df[df['text_clean'].str.contains(keyword_list[0]) | df['text_clean'].str.contains(keyword_list[1]) | df['text_clean'].str.contains(keyword_list[2])
        | df['text_clean'].str.contains(keyword_list[3]) | df['text_clean'].str.contains(keyword_list[4]) | df['text_clean'].str.contains(keyword_list[5])]
    return df


def map_strict(user_input, user_event):
    fig = px.scatter_mapbox(strict_matches_df(user_input, user_event), lat = 'lat', lon = 'long',
                        color_discrete_sequence = ['navy'],hover_data = ['text_clean'], zoom = 3, height = 500)
    fig.update_layout(mapbox_style = 'open-street-map')
    fig.update_layout(margin = {'r': 0, 't': 0, 'l': 0, 'b':0})
    pyo.iplot(fig)
    return fig.write_html('./flask_map1.html')

def map_loose(user_input, user_event):
    fig = px.scatter_mapbox(loose_matches_df(user_input, user_event), lat = 'lat', lon = 'long',
                        color_discrete_sequence = ['navy'],hover_data = ['text_clean'], zoom = 3, height = 500)
    fig.update_layout(mapbox_style = 'open-street-map')
    fig.update_layout(margin = {'r': 0, 't': 0, 'l': 0, 'b':0})
    pyo.iplot(fig)
    return fig.write_html('./flask_map1.html')
