from typing import Union
import pandas as pd
import numpy as np
import panel as pn
pn.extension('tabulator')
import hvplot.pandas
import calendar
import networkx as nx
import matplotlib.pyplot as plt

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(uvicorn=True)

df = pd.read_csv("data_testing.csv")
final_discussion_data = pd.read_csv("final_github_discussion_data.csv")
autoware_membership_data = pd.read_csv("autoware_contributors.csv")

idf = df.interactive()
ifinal_discussions_data = final_discussion_data.interactive()
iautoware_membership_data = autoware_membership_data.interactive()

# pulls_per_repo = (
#     idf.groupby(['Repository'])
#     .size()
#     .reset_index(name='Pull_Request_Count')
#     .set_index(['Repository'])
#     .sort_values(by=['Pull_Request_Count'], ascending=False)
# )
# pulls_per_repo

pulls_per_repo = (
    df.groupby(['Repository'])
    .size()
    .reset_index(name='Pull_Request_Count')
    .set_index(['Repository'])
    .sort_values(by=['Pull_Request_Count'], ascending=False)
)
# pulls_per_repo

open_pulls_per_repo = (
    # only include open pull requests
    idf[idf['PR_Status'] == 'open']
    .groupby(['Repository'])
    .size()
    .reset_index(name='Open_Pull_Request_Count')
    .set_index(['Repository'])
    .sort_values(by=['Open_Pull_Request_Count'], ascending=False)
)
open_pulls_per_repo

# df['Start_time'] = df['Start_time'].apply(lambda x: '{0:0>2}'.format(x))
# df['Start_month'] = df['Start_month'].apply(lambda x: '{0:0>2}'.format(x))
# df['Start_year_month'] = df['Start_year'].astype(str) + '-' + df['Start_month'].astype(str)
months_dict = {k: v for k,v in enumerate(calendar.month_abbr)}

df['Start_month'] = df['Start_time'].apply(lambda x: months_dict.get(int(x.split(' ')[0].split('-')[1])))
df['Start_year_month'] = df['Start_time'].apply(lambda x: x.split(' ')[0].split('-')[0]) + '-' + df['Start_month'].astype(str)

pulls_per_month = (
    idf.groupby(['Start_year_month'])
    .size()
    .reset_index(name='Monthly_Pulls')
    .set_index(['Start_year_month'])
    .sort_values(by=['Start_year_month'], ascending=True)
)
pulls_per_month

# filter out rows with NaN End_time values

df = df[df['End_time'].notna()]

# calculate the time to merge for each pull request in days

df['Days_to_Merge'] = (pd.to_datetime(df['End_time']) - pd.to_datetime(df['Start_time'])).dt.days

# sort rows by End_time

df = df.sort_values(by=['End_time'], ascending=True)

# calculate the rolling average of time to merge for each pull request in days

df['Rolling_Avg_Days_to_Merge'] = df['Days_to_Merge'].rolling(window=100).mean()

# remove the first 99 rows (which have NaN values for the rolling average)

df = df.iloc[99:]

# App endpoints

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
def test_func():
    return "Reached test endpoint"

@app.get("/sample_endpoint")
def sample_endpoint_func():
    return pulls_per_repo.head(100).to_dict(orient='records')

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/get_pulls_per_repo")
def get_pulls_per_repo():
    return pulls_per_repo.to_dict(orient='records')

@app.get("/open_pulls_per_repo")
def get_open_pulls():
    return open_pulls_per_repo.to_dict(orient='records')

@app.get("/pulls_per_month")
def get_pulls_per_month():
    return pulls_per_month.to_dict(orient='records')

@app.get("/rolling_avg_days_to_merge")
def get_rolling_avg_days_to_merge():
    return df['Rolling_Avg_Days_to_Merge'].to_dict()

@app.get("/get_discussion_data")
def get_discussion_data():
    # This following section contains the wrangling code for the discussion data (which will be joined with the membership data)

    # Join the autoware contributors CSV with the final discussion data CSV to get inter-organization metrics
    full_autoware_data = pd.merge(final_discussion_data, autoware_membership_data, left_on='discussion_comment_author', right_on='Github username', how='inner')
    full_autoware_data = full_autoware_data.drop("Autoware expertise list", axis=1)

    full_autoware_data = full_autoware_data.dropna(subset='Name')
    full_autoware_data['Organisation'] = full_autoware_data['Organisation'].apply(lambda x: x.split(", "))
    full_autoware_data = full_autoware_data.explode('Organisation')

    # Drop rows where discussion_thread_author_id is the same as discussion_comment_author
    full_autoware_data_unique = full_autoware_data[full_autoware_data['discussion_thread_author_id'] != full_autoware_data['discussion_comment_author']]
    full_autoware_data_unique = full_autoware_data_unique.rename(columns={"Name": "Commenter Name", "Organisation": "Commenter Organisation"})

    full_autoware_data_unique_w_orgs = pd.merge(full_autoware_data_unique, autoware_membership_data, left_on='discussion_thread_author_id', right_on='Github username', how='inner')
    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.drop(columns=['Autoware expertise list', 'Gitlab username_x', 'Gitlab username_y'])
    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.rename(columns={"Organisation": "Discussion Thread Author Organisation", "Github username_x": "Commenter Github Username", "Github username_y": "Discussion Thread Author Github Username"})

    full_autoware_data_unique_w_orgs['Commenter Organisation'] = full_autoware_data_unique_w_orgs['Commenter Organisation'].replace(["Autocore.ai   "], ["Autocore.ai"])
    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.dropna(subset='Discussion Thread Author Organisation')
    full_autoware_data_unique_w_orgs['Discussion Thread Author Organisation'] = full_autoware_data_unique_w_orgs['Discussion Thread Author Organisation'].apply(lambda x: x.split(", "))
    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.explode('Discussion Thread Author Organisation')

    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.rename(columns={"Name": "Discussion Thread Author Name"})

    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.drop(full_autoware_data_unique_w_orgs[full_autoware_data_unique_w_orgs['Commenter Organisation'] == 'Autocore.ai   '].index)
    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.drop(full_autoware_data_unique_w_orgs[full_autoware_data_unique_w_orgs['Discussion Thread Author Organisation'] == 'Autocore.ai   '].index)

    commenter_orgs = list(full_autoware_data_unique_w_orgs['Commenter Organisation'].unique())
    dta_orgs = list(full_autoware_data_unique_w_orgs['Discussion Thread Author Organisation'].unique())

    unique_orgs = list(set(commenter_orgs + dta_orgs))

    autoware_network_diff_orgs = full_autoware_data_unique_w_orgs[full_autoware_data_unique_w_orgs['Discussion Thread Author Organisation'] != full_autoware_data_unique_w_orgs['Commenter Organisation']].reset_index(drop=True)
    commenter_DTA_gb_df = autoware_network_diff_orgs.groupby(by=['Commenter Organisation', 'Discussion Thread Author Organisation'])['discussion_title'].count().reset_index(name='Commenter DTA Connection Count')

    # Again use the nx library to created a directed graph (DiGraph) that we can then use to run PageRank/Gini coefficient analyses
    # and generate other networked level metrics
    G2 = nx.DiGraph()

    # Create a dictionary that can be used to keep track of the number of connections from an organization to another
    org_connection_count_dict = {}

    # Iterate through autoware_network_diff_orgs to create a sample network
    for index, row in commenter_DTA_gb_df.iterrows():
        commenter_org = row["Commenter Organisation"]
        dta_org = row["Discussion Thread Author Organisation"]

        commenter_dta_count = row['Commenter DTA Connection Count']

    if commenter_dta_count > 30:
        G2.add_edge(commenter_org, dta_org, weight=commenter_dta_count)
        org_connection_count_dict.update({(commenter_org, dta_org): commenter_dta_count})


    # # To list the values of weights along each edge
    # for src, tgt, data in G2.edges(data=True):
    #     edge_weight = data['weight']
    #     print(f"Edge from {src} to {tgt} has weight {edge_weight}")

    # To print the names of all nodes
    all_nodes = list(G2.nodes())

    # Draw the graph
    pos = nx.circular_layout(G2)
    labels = {node: node for node in all_nodes}
    plt.figure(figsize=(18, 20))  # Adjust the figure size as needed

    nx.draw_networkx_nodes(G2, pos, node_size=400, node_color='skyblue')
    nx.draw_networkx_labels(G2, pos, labels=labels, font_size=10, font_color='black')

    # nx.draw(G2, pos, with_labels=True, labels=labels, node_size=1000, node_color='skyblue', font_size=10, font_color='black')

    edge_labels = {(src, tgt): data['weight'] for src, tgt, data in G2.edges(data=True)}
    nx.draw_networkx_edges(G2, pos)
    nx.draw_networkx_edge_labels(G2, pos, edge_labels=edge_labels, font_size=8, font_color='red')

    plt.title("Commenter-DTA Connection Network Across Organizations")
    plt.show()

    for k, v in org_connection_count_dict.items():
        print(k, v)    
