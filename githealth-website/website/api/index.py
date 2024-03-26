from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import os
import glob
import networkx as nx
import io
import matplotlib.pyplot as plt
import math
import datetime
from datetime import date
from typing import List, Optional
from fastapi import Query
from collections import defaultdict
from networkx.algorithms import community

from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine, EdgesAndLinkedNodes, NodesAndLinkedEdges, LabelSet
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Turbo256
from networkx.algorithms import community

from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.resources import CDN 
from bokeh.embed import json_item

import bokeh.io
import bokeh.plotting
from bokeh.palettes import Category20, Reds8

from fastapi.responses import HTMLResponse, JSONResponse
import json

app = FastAPI()

# Set up CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define a Pydantic model for the response data structure
# TODO: Rename
class IssueResponseTime(BaseModel):
    year: int
    month: int
    issues_time_to_first_response_hours: float


class IssueResponseDate(BaseModel):
    date: datetime.date
    issues_time_to_first_response_hours: float


class IssueCloseTime(BaseModel):
    year: int
    month: int
    issues_time_to_close_hours: float


class IssueCloseDate(BaseModel):
    date: datetime.date
    issues_time_to_close_hours: float


class CommentCountByDiscussionThreadAuthor(BaseModel):
    discussion_thread_author: str
    comment_author: str
    comment_count: int
    normalized_comment_count: float


class CommenterDTAConnectionCountAcrossOrganizations(BaseModel):
    commenter_organization: str
    discussion_thread_author_organization: str
    commenter_dta_connection_count: int

class UserContribution(BaseModel):
    user: str
    user_affiliation: str
    issues_created: int
    issues_commented: int
    average_time_to_first_response_hours: float
    average_time_to_close_hours: float
    total_comments: int
    total_commits: int
    total_checks: int
    total_files_changed: int
    total_lines_changed: int

def get_user_contributions() -> List[UserContribution]:
    # Read the CSV file into a DataFrame
    df = pd.read_csv("Issues_Data/issues_data+users_v7.0/final_merged_issues_data.csv")

    # Convert time-related columns from seconds to hours
    df['issues_time_to_first_response_hours'] = df['issues_time_to_first_response'] / 3600
    df['issues_time_to_close_hours'] = df['issues_time_to_close'] / 3600

    # Aggregate data by issue creator
    issues_by_creator = df.groupby(['issues_thread_creator', 'issues_thread_creator_affiliation']).agg({
        'issues_title': 'count',
        'issues_time_to_first_response_hours': 'mean',
        'issues_time_to_close_hours': 'mean'
    }).rename(columns={
        'issues_title': 'issues_created',
        'issues_time_to_first_response_hours': 'average_time_to_first_response_hours',
        'issues_time_to_close_hours': 'average_time_to_close_hours'
    }).reset_index()

    # Aggregate data by comment author
    comments_by_author = df.groupby(['issues_comment_author', 'issues_comment_author_affiliation']).agg({
        'issues_comment_id': 'count',
        'issues_commits': 'sum',
        'issues_checks': 'sum',
        'issues_files_changed': 'sum',
        'issues_lines_changed': 'sum'
    }).rename(columns={
        'issues_comment_id': 'issues_commented',
        'issues_commits': 'total_commits',
        'issues_checks': 'total_checks',
        'issues_files_changed': 'total_files_changed',
        'issues_lines_changed': 'total_lines_changed'
    }).reset_index()

    # Merge the dataframes on the user identifier
    contributions = pd.merge(
        issues_by_creator,
        comments_by_author,
        left_on=['issues_thread_creator', 'issues_thread_creator_affiliation'],
        right_on=['issues_comment_author', 'issues_comment_author_affiliation'],
        how='outer'
    )

    # Fill NaN values with 0 for users who may have created issues but made no comments (or vice versa)
    contributions.fillna(0, inplace=True)

    # Create a combined user and affiliation column
    contributions['user'] = contributions.apply(
        lambda row: row['issues_thread_creator'] or row['issues_comment_author'], axis=1
    )
    contributions['user_affiliation'] = contributions.apply(
        lambda row: row['issues_thread_creator_affiliation'] or row['issues_comment_author_affiliation'], axis=1
    )

    # Prepare the final list of Pydantic models
    user_contributions = [
        UserContribution(
            user=row['user'],
            user_affiliation=row['user_affiliation'],
            issues_created=row['issues_created'],
            issues_commented=row['issues_commented'],
            average_time_to_first_response_hours=row['average_time_to_first_response_hours'],
            average_time_to_close_hours=row['average_time_to_close_hours'],
            total_comments=row['issues_commented'],  # Assuming issues_commented represents the total comments made
            total_commits=row['total_commits'],
            total_checks=row['total_checks'],
            total_files_changed=row['total_files_changed'],
            total_lines_changed=row['total_lines_changed']
        )
        for index, row in contributions.iterrows()
    ]

    return user_contributions

@app.get("/users/contributions", response_model=List[UserContribution])
async def users_contributions():
    contributions = get_user_contributions()
    return contributions

class OrganizationContribution(BaseModel):
    organization: str
    issues_created: int
    issues_commented: int
    average_time_to_first_response_hours: float
    average_time_to_close_hours: float
    total_comments: int
    total_commits: int
    total_checks: int
    total_files_changed: int
    total_lines_changed: int

def get_organization_contributions() -> List[OrganizationContribution]:
    # Read the CSV file into a DataFrame
    df = pd.read_csv("Issues_Data/issues_data+users_v7.0/final_merged_issues_data.csv")

    # Convert time-related columns from seconds to hours
    df['issues_time_to_first_response_hours'] = df['issues_time_to_first_response'] / 3600
    df['issues_time_to_close_hours'] = df['issues_time_to_close'] / 3600

    # Aggregate data by issue creator's affiliation
    issues_by_org = df.groupby('issues_thread_creator_affiliation').agg({
        'issues_title': 'count',
        'issues_time_to_first_response_hours': 'mean',
        'issues_time_to_close_hours': 'mean'
    }).rename(columns={
        'issues_title': 'issues_created',
        'issues_time_to_first_response_hours': 'average_time_to_first_response_hours',
        'issues_time_to_close_hours': 'average_time_to_close_hours'
    }).reset_index()

    # Aggregate data by comment author's affiliation
    comments_by_org = df.groupby('issues_comment_author_affiliation').agg({
        'issues_comment_id': 'count',
        'issues_commits': 'sum',
        'issues_checks': 'sum',
        'issues_files_changed': 'sum',
        'issues_lines_changed': 'sum'
    }).rename(columns={
        'issues_comment_id': 'issues_commented',
        'issues_commits': 'total_commits',
        'issues_checks': 'total_checks',
        'issues_files_changed': 'total_files_changed',
        'issues_lines_changed': 'total_lines_changed'
    }).reset_index()

    # Merge the dataframes on the organization
    contributions = pd.merge(
        issues_by_org,
        comments_by_org,
        left_on='issues_thread_creator_affiliation',
        right_on='issues_comment_author_affiliation',
        how='outer'
    )

    # Fill NaN values with 0 for organizations that may have created issues but made no comments (or vice versa)
    contributions.fillna(0, inplace=True)

    # Prepare the final list of Pydantic models
    org_contributions = [
        OrganizationContribution(
            organization=row['issues_thread_creator_affiliation'] or row['issues_comment_author_affiliation'],
            issues_created=row['issues_created'],
            issues_commented=row['issues_commented'],
            average_time_to_first_response_hours=row['average_time_to_first_response_hours'],
            average_time_to_close_hours=row['average_time_to_close_hours'],
            total_comments=row['issues_commented'],  # Assuming issues_commented represents the total comments made
            total_commits=row['total_commits'],
            total_checks=row['total_checks'],
            total_files_changed=row['total_files_changed'],
            total_lines_changed=row['total_lines_changed']
        )
        for index, row in contributions.iterrows()
    ]

    return org_contributions

@app.get("/organizations/contributions", response_model=List[OrganizationContribution])
async def organizations_contributions():
    contributions = get_organization_contributions()
    return contributions


# Calculate issue data a single time:
# TODO: add some sort of timed caching method:
response_times: List[IssueResponseTime] = []
close_times: List[IssueCloseTime] = []


def get_response_times():
    global response_times
    if len(response_times) != 0:
        return response_times

    # # TODO: Use database instead of CSV
    # csv_dir = "Issues_Data/issues_data+users_v7.0"
    # csv_pattern = os.path.join(csv_dir, 'final_merged_issues_data.csv')
    # csv_files = glob.glob(csv_pattern)

    # Read the CSV file into a DataFrame
    df = pd.read_csv("Issues_Data/issues_data+users_v7.0/final_merged_issues_data.csv")
    # Convert 'issues_created_at' column to datetime
    df["issues_created_at"] = pd.to_datetime(df["issues_created_at"], errors="coerce")
    # Drop rows with invalid datetime conversion
    df = df.dropna(subset=["issues_created_at"])
    # Drop rows with NaN in 'issues_time_to_first_response'
    df = df.dropna(subset=["issues_time_to_first_response"])
    # Drop duplicate issue threads
    df = df.drop_duplicates(subset=["issues_thread_id"])
    # Extract year and month from 'issues_created_at'
    df["year"] = df["issues_created_at"].dt.year
    df["month"] = df["issues_created_at"].dt.month
    # Set a threshold to filter out automatic responses
    threshold_seconds = 5
    df = df[df["issues_time_to_first_response"] > threshold_seconds]

    if df.empty:
        raise HTTPException(status_code=404, detail="No issues data found")

    # Calculate the average time to first response in hours
    df["issues_time_to_first_response_hours"] = df["issues_time_to_first_response"] / 3600

    sorted_issues_data = df.sort_values(by=["year", "month"])
    response_data = sorted_issues_data[["year", "month", "issues_time_to_first_response_hours"]]

    # Convert the pandas DataFrame to a list of dictionaries
    response_times = response_data.to_dict(orient="records")

    return response_times


@app.get("/issues/first-response-time/mean", response_model=List[IssueResponseDate])
async def first_response_mean(
    start_date: Optional[date] = Query(None), end_date: Optional[date] = Query(None)
):
    response_times = get_response_times()
    df = pd.DataFrame(response_times)

    # Convert 'date' column to datetime object
    df["date"] = pd.to_datetime(df.assign(day=1)[["year", "month", "day"]])

    # Filter data based on start_date and end_date
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]

    # Group by date and calculate the average time to first response
    monthly_avg = (
        df.groupby("date")["issues_time_to_first_response_hours"].mean().reset_index()
    )
    return monthly_avg.to_dict(orient="records")


@app.get("/issues/first-response-time/median", response_model=List[IssueResponseDate])
async def first_response_median():
    response_times = get_response_times()
    df = pd.DataFrame(response_times)

    # Group by year and month, then calculate the average time to first response
    monthly_avg = (
        df.groupby(["year", "month"])["issues_time_to_first_response_hours"]
        .median()
        .reset_index()
    )

    # Convert 'year' and 'month' into a datetime object
    monthly_avg["date"] = pd.to_datetime(
        monthly_avg.assign(day=1)[["year", "month", "day"]]
    )

    monthly_avg.drop(columns=["year", "month"], inplace=True)

    monthly_avg = monthly_avg.reindex(
        columns=["date", "issues_time_to_first_response_hours"]
    )
    return monthly_avg.to_dict(orient="records")


def get_close_times():
    df = pd.read_csv("Issues_Data/issues_data+users_v7.0/final_merged_issues_data.csv")

    df["issues_created_at"] = pd.to_datetime(df["issues_created_at"], errors="coerce")
    df = df.dropna(subset=["issues_created_at", "issues_time_to_close"])
    df = df.drop_duplicates(subset=["issues_thread_id"])
    df["year"] = df["issues_created_at"].dt.year
    df["month"] = df["issues_created_at"].dt.month
    df = df[df["issues_time_to_close"] > 5]  # Using 5 seconds as the threshold
    df["issues_time_to_close_hours"] = df["issues_time_to_close"] / 3600

    sorted_issues_data = df.sort_values(by=["year", "month"])
    close_data = sorted_issues_data[["year", "month", "issues_time_to_close_hours"]]

    # Convert the pandas DataFrame to a list of dictionaries
    close_times = close_data.to_dict(orient="records")

    return close_times


@app.get("/issues/close-time/mean", response_model=List[IssueCloseDate])
async def close_time_mean():
    close_times = get_close_times()
    df = pd.DataFrame(close_times)

    # Group by year and month, then calculate the average time to first response
    monthly_avg = (
        df.groupby(["year", "month"])["issues_time_to_close_hours"].mean().reset_index()
    )

    # Convert 'year' and 'month' into a datetime object
    monthly_avg["date"] = pd.to_datetime(
        monthly_avg.assign(day=1)[["year", "month", "day"]]
    )

    monthly_avg.drop(columns=["year", "month"], inplace=True)

    monthly_avg = monthly_avg.reindex(columns=["date", "issues_time_to_close_hours"])
    return monthly_avg.to_dict(orient="records")


@app.get("/issues/close-time/median", response_model=List[IssueCloseDate])
async def close_time_median():
    close_times = get_close_times()
    df = pd.DataFrame(close_times)

    # Group by year and month, then calculate the average time to first response
    monthly_avg = (
        df.groupby(["year", "month"])["issues_time_to_close_hours"]
        .median()
        .reset_index()
    )

    # Convert 'year' and 'month' into a datetime object
    monthly_avg["date"] = pd.to_datetime(
        monthly_avg.assign(day=1)[["year", "month", "day"]]
    )

    monthly_avg.drop(columns=["year", "month"], inplace=True)

    monthly_avg = monthly_avg.reindex(columns=["date", "issues_time_to_close_hours"])
    return monthly_avg.to_dict(orient="records")


# Comment count by discussion thread author
@app.get(
    "/discussions/comment-count-by-discussion-thread-author",
    response_model=None,
)
async def generate_comment_countdiscussion_thread_author_table():
    discussion_data = pd.read_csv("Discussions_Data/github_discussion_data.csv")

    # We want to primarily focus on those discussions that have been answered - those are the most informative
    answered_discussion_data = discussion_data[
        discussion_data["Answered/Unanswered"] == "Answered"
    ]

    # This gives us the user IDs of those whose discussions generate the most comments
    gb_df_1 = (
        answered_discussion_data.groupby("User ID")["Comment Author"]
        .count()
        .reset_index()
    )
    gb_df_1 = gb_df_1[gb_df_1["User ID"] != "Unknown"]
    gb_df_1 = gb_df_1.sort_values(
        by="Comment Author", ascending=False, ignore_index=True
    )

    # This groupby generates the number of comments specific individuals make on a certain person's discussions
    # (can be used to measure collaboration index and define weight edges for a graph when normalized)
    gb_df_2 = (
        answered_discussion_data.groupby(["User ID", "Comment Author"])["Comment ID"]
        .count()
        .reset_index()
    )
    gb_df_2 = gb_df_2[gb_df_2["User ID"] != gb_df_2["Comment Author"]]
    gb_df_2 = gb_df_2[
        (gb_df_2["User ID"] != "Unknown") & (gb_df_2["Comment Author"] != "Unknown")
    ]
    gb_df_2 = gb_df_2.sort_values(by="Comment ID", ascending=False, ignore_index=True)

    # Could be used for PageRank initialization
    total_comments = gb_df_2["Comment ID"].sum()
    gb_df_2["Normalized Comment ID"] = gb_df_2["Comment ID"] / total_comments

    gb_df_2 = gb_df_2.rename(
        columns={
            "User ID": "discussion_thread_author",
            "Comment Author": "comment_author",
            "Comment ID": "comment_count",
            "Normalized Comment ID": "normalized_comment_count",
        }
    )
    # gb_df_2 = gb_df_2[gb_df_2["comment_count"] > 5]

    # Set a threshold for comment_count
    comment_count_threshold = 3

    # Filter the DataFrame based on the threshold
    filtered_df = gb_df_2[gb_df_2['comment_count'] > comment_count_threshold]

    # Generate the network graph
    G_new = nx.from_pandas_edgelist(filtered_df, 'discussion_thread_author', 'comment_author', ['comment_count', 'normalized_comment_count'])

    # Create a dictionary that can be used to keep track of the number of connections from an individual to another
    indiv_connection_count_dict = defaultdict(list)

    # Iterate through filtered_df to create a sample network
    for _, row in filtered_df.iterrows():
        commenter = row["comment_author"]
        dta = row["discussion_thread_author"]
        commenter_dta_count = row['comment_count']

        indiv_connection_count_dict[dta].append(f"{commenter}:{commenter_dta_count}")

    # Sort each list in org_connection_count_dict
    for dta in indiv_connection_count_dict.keys():
        indiv_connection_count_dict[dta] = sorted(indiv_connection_count_dict[dta], key=lambda x: int(x.split(":")[1]), reverse=True)

    # Calculate the betweenness centrality for each node, as well as the weighted degree metric
    betweenness_centrality_dict_new = nx.betweenness_centrality(G_new, weight='normalized_comment_count')
    nx.set_node_attributes(G_new, name='betweenness', values=betweenness_centrality_dict_new)

    # nx.degree(G2, weight='commenter_dta_connection_count')
    # weighted_degree_dict = dict(nx.degree(G2, weight='commenter_dta_connection_count'))
    nx.set_node_attributes(G_new, name='weighted_degree', values=indiv_connection_count_dict)

    # Now, determine what are the distinct communities within the network
    communities_G_new = community.greedy_modularity_communities(G_new)

    # Create empty dictionary
    modularity_class_G_new = {}
    modularity_color_G_new = {}

    # Loop through each community in the network
    for community_number, comm in enumerate(communities_G_new):
        # For each member of the community, add their community number
        for name in comm:
            modularity_class_G_new[name] = community_number
            modularity_color_G_new[name] = Turbo256[community_number*8]

    nx.set_node_attributes(G_new, modularity_class_G_new, 'modularity_class')
    nx.set_node_attributes(G_new, modularity_color_G_new, 'modularity_color')
    color_attr = 'modularity_color'

    title = 'Initializer-Commenter Relationship Network'

    hover_vals_new = [
        ("Organization", "@index"),
        ("Betweenness", "@betweenness"),
        ("Most Frequent Commenters", "@weighted_degree"),
        ("Modularity Color", "$color[swatch]:modularity_color")
    ]

    plot_new = figure(tooltips = hover_vals_new, active_scroll='wheel_zoom',
                x_range=Range1d(-20.1, 20.1), y_range=Range1d(-20.1, 20.1), title=title)

    # Create a network graph object with the corrected layout
    mapping_new = dict((n, i) for i, n in enumerate(G_new.nodes))
    H_new = nx.relabel_nodes(G_new, mapping_new)
    network_new = from_networkx(H_new, nx.fruchterman_reingold_layout, scale=150, center=(0, 0))

    # Use node_renderer to attach hover tool
    network_new.node_renderer.glyph = Circle(size=10, fill_color=color_attr)
    network_new.node_renderer.hover_glyph = Circle(size=10, fill_color='white', line_width=2)
    network_new.node_renderer.selection_glyph = Circle(size=10, fill_color='white', line_width=2)

    # Customize the hover tool to filter by dta_org
    hover_new = HoverTool(
        tooltips=hover_vals_new,
        renderers=[network_new.node_renderer],  # Use node_renderer for hover tool
        mode='mouse'
    )

    x_new, y_new = zip(*network_new.layout_provider.graph_layout.values())
    node_labels_new = list(G_new.nodes())
    src_new = ColumnDataSource({'x': x_new, 'y': y_new, 'name': [node_labels_new[i] for i in range(len(x_new))]})
    lbls_new = LabelSet(x='x', y='y', text='name', source=src_new, background_fill_color='white', text_font_size='10px', background_fill_alpha=.9)
    plot_new.renderers.append(lbls_new)

    # Add the hover tool to the plot
    plot_new.add_tools(hover_new)

    network_new.edge_renderer.glyph = MultiLine(line_alpha=0.3, line_width=1)
    network_new.edge_renderer.selection_glyph = MultiLine(line_color='black', line_width=2)
    network_new.edge_renderer.hover_glyph = MultiLine(line_color='black', line_width=2)

    network_new.selection_policy = NodesAndLinkedEdges()
    network_new.inspection_policy = NodesAndLinkedEdges()

    plot_new.renderers.append(network_new)

    # show(plot_new)

    # # Now, use the nx library to created a directed graph (DiGraph) that we can then use to run PageRank/Gini coefficient analyses
    # # and generate other networked level metrics
    # G = nx.DiGraph()

    # # Iterate through gb_df_2 to create a sample network and
    # for index, row in gb_df_2.iterrows():
    #     src_node = row["discussion_thread_author"]
    #     tgt_node = row["comment_author"]
    #     weight = row["normalized_comment_count"]

    # if weight > 0.002:
    #     G.add_edge(src_node, tgt_node, weight=weight)

    # # # To list the values of weights along each edge
    # # for src, tgt, data in G.edges(data=True):
    # #     edge_weight = data['weight']
    # #     print(f"Edge from {src} to {tgt} has weight {edge_weight}")

    # # To print the names of all nodes
    # all_nodes = list(G.nodes())

    # # Draw the graph
    # pos = nx.spring_layout(G, k=0.25)  # You can experiment with the 'k' parameter
    # labels = {node: node for node in all_nodes}
    # plt.figure(figsize=(18, 20))  # Adjust the figure size as needed
    # nx.draw(G, pos, with_labels=True, labels=labels, node_size=1000, node_color='skyblue', font_size=10, font_color='black')
    # edge_labels = {(src, tgt): round(data['weight'], 5) for src, tgt, data in G.edges(data=True)}
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='red')
    # plt.title("Initializer-Commenter Relationship Network, using Normalized Weights")
    # plt.show()

    # Convert the pandas DataFrame to a list of dictionaries
    response_list = filtered_df.to_dict(orient="records")

    return JSONResponse(content={'plot_json': json_item(plot_new, "commenter_dta_connection_network"), 'response_list': response_list})
    # return json_item(plot_new, "commenter_dta_connection_network"), response_list

    # Bokeh plot creation code (replace the show(plot_new) with the following):
    # script, div = components(plot_new, wrap_script=False)
    # print(div)

    # # CDN lines
    # cdn_js = CDN.js_files[0]
    # print(cdn_js)

    # # # Include other relevant information you want to send to the frontend
    # response_info = {
    #     "script": script,
    #     "div": div,
    #     "cdn_js": cdn_js,
    #     "response_list": response_list
    # }

    # # Convert the Bokeh plot to JSON
    # plot_json = json.dumps(json_item(plot_new, "myplot"))

    # return JSONResponse(content={'plot_json': plot_json})

    # return response_info

    # return response_list


# Commenter DTA connection count across organizations
@app.get(
    "/discussions/commenter-dta-connection-count-across-organizations",
    response_model=List[CommenterDTAConnectionCountAcrossOrganizations],
)
async def generate_commenter_dta_connection_count_across_organizations():
    final_discussion_data = pd.read_csv(
        "Discussions_Data/final_github_discussion_data.csv"
    )
    autoware_membership_data = pd.read_csv("Discussions_Data/autoware_contributors.csv")

    # Join the autoware contributors CSV with the final discussion data CSV to get inter-organization metrics
    full_autoware_data = pd.merge(
        final_discussion_data,
        autoware_membership_data,
        left_on="discussion_comment_author",
        right_on="Github username",
        how="inner",
    )
    full_autoware_data = full_autoware_data.drop("Autoware expertise list", axis=1)

    full_autoware_data = full_autoware_data.dropna(subset="Name")
    full_autoware_data["Organisation"] = full_autoware_data["Organisation"].apply(
        lambda x: x.split(", ")
    )
    full_autoware_data = full_autoware_data.explode("Organisation")

    # Drop rows where discussion_thread_author_id is the same as discussion_comment_author
    full_autoware_data_unique = full_autoware_data[
        full_autoware_data["discussion_thread_author_id"]
        != full_autoware_data["discussion_comment_author"]
    ]
    full_autoware_data_unique = full_autoware_data_unique.rename(
        columns={"Name": "Commenter Name", "Organisation": "Commenter Organisation"}
    )

    full_autoware_data_unique_w_orgs = pd.merge(
        full_autoware_data_unique,
        autoware_membership_data,
        left_on="discussion_thread_author_id",
        right_on="Github username",
        how="inner",
    )
    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.drop(
        columns=["Autoware expertise list", "Gitlab username_x", "Gitlab username_y"]
    )
    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.rename(
        columns={
            "Organisation": "Discussion Thread Author Organisation",
            "Github username_x": "Commenter Github Username",
            "Github username_y": "Discussion Thread Author Github Username",
        }
    )

    full_autoware_data_unique_w_orgs[
        "Commenter Organisation"
    ] = full_autoware_data_unique_w_orgs["Commenter Organisation"].replace(
        ["Autocore.ai   "], ["Autocore.ai"]
    )
    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.dropna(
        subset="Discussion Thread Author Organisation"
    )
    full_autoware_data_unique_w_orgs[
        "Discussion Thread Author Organisation"
    ] = full_autoware_data_unique_w_orgs["Discussion Thread Author Organisation"].apply(
        lambda x: x.split(", ")
    )
    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.explode(
        "Discussion Thread Author Organisation"
    )

    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.rename(
        columns={"Name": "Discussion Thread Author Name"}
    )

    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.drop(
        full_autoware_data_unique_w_orgs[
            full_autoware_data_unique_w_orgs["Commenter Organisation"]
            == "Autocore.ai   "
        ].index
    )
    full_autoware_data_unique_w_orgs = full_autoware_data_unique_w_orgs.drop(
        full_autoware_data_unique_w_orgs[
            full_autoware_data_unique_w_orgs["Discussion Thread Author Organisation"]
            == "Autocore.ai   "
        ].index
    )

    # Analyze connections between commenters and discussion thread authors

    # First, get all unique organizations anyone is a part of
    commenter_orgs = list(
        full_autoware_data_unique_w_orgs["Commenter Organisation"].unique()
    )
    dta_orgs = list(
        full_autoware_data_unique_w_orgs[
            "Discussion Thread Author Organisation"
        ].unique()
    )

    unique_orgs = list(set(commenter_orgs + dta_orgs))

    autoware_network_diff_orgs = full_autoware_data_unique_w_orgs[
        full_autoware_data_unique_w_orgs["Discussion Thread Author Organisation"]
        != full_autoware_data_unique_w_orgs["Commenter Organisation"]
    ].reset_index(drop=True)

    commenter_DTA_gb_df = (
        autoware_network_diff_orgs.groupby(
            by=["Commenter Organisation", "Discussion Thread Author Organisation"]
        )["discussion_title"]
        .count()
        .reset_index(name="Commenter DTA Connection Count")
    )
    commenter_DTA_gb_df = commenter_DTA_gb_df.sort_values(
        by="Commenter DTA Connection Count", ascending=False, ignore_index=True
    )

    commenter_DTA_gb_df = commenter_DTA_gb_df.rename(
        columns={
            "Commenter Organisation": "commenter_organization",
            "Discussion Thread Author Organisation": "discussion_thread_author_organization",
            "Commenter DTA Connection Count": "commenter_dta_connection_count",
        }
    )

    # # Enable viewing Bokeh plots in the notebook
    # bokeh.io.output_notebook()

    # Generate the network graph
    G2 = nx.from_pandas_edgelist(commenter_DTA_gb_df, 'commenter_organization', 'discussion_thread_author_organization', 'commenter_dta_connection_count')

    # Create a dictionary that can be used to keep track of the number of connections from an organization to another
    org_connection_count_dict = defaultdict(list)

    # Iterate through autoware_network_diff_orgs to create a sample network
    for _, row in commenter_DTA_gb_df.iterrows():
        commenter_org = row["commenter_organization"]
        dta_org = row["discussion_thread_author_organization"]
        commenter_dta_count = row['commenter_dta_connection_count']

        org_connection_count_dict[dta_org].append(f"{commenter_org}:{commenter_dta_count}")

    # Sort each list in org_connection_count_dict
    for dta_org in org_connection_count_dict.keys():
        org_connection_count_dict[dta_org] = sorted(org_connection_count_dict[dta_org], key=lambda x: int(x.split(":")[1]), reverse=True)

    # Calculate the betweenness centrality for each node, as well as the weighted degree metric
    betweenness_centrality_dict = nx.betweenness_centrality(G2, weight='commenter_dta_connection_count')
    nx.set_node_attributes(G2, name='betweenness', values=betweenness_centrality_dict)

    # nx.degree(G2, weight='commenter_dta_connection_count')
    # weighted_degree_dict = dict(nx.degree(G2, weight='commenter_dta_connection_count'))
    nx.set_node_attributes(G2, name='weighted_degree', values=org_connection_count_dict)

    # Now, determine what are the distinct communities within the network
    communities = community.greedy_modularity_communities(G2)

    # Create empty dictionary
    modularity_class = {}
    modularity_color = {}

    # Loop through each community in the network
    for community_number, comm in enumerate(communities):
        # For each member of the community, add their community number
        for name in comm:
            modularity_class[name] = community_number
            modularity_color[name] = Reds8[community_number*3]

    nx.set_node_attributes(G2, modularity_class, 'modularity_class')
    nx.set_node_attributes(G2, modularity_color, 'modularity_color')
    color_attr = 'modularity_color'

    title = 'Commenter-DTA Connection Network Across Organizations'

    hover_vals = [
        ("Organization", "@index"),
        ("Betweenness", "@betweenness"),
        ("Most Frequent Commenters by Organization", "@weighted_degree"),
        ("Modularity Color", "$color[swatch]:modularity_color")
    ]

    plot = figure(tooltips = hover_vals, active_scroll='wheel_zoom',
                x_range=Range1d(-20.1, 20.1), y_range=Range1d(-20.1, 20.1), title=title)

    # Create a network graph object with the corrected layout
    mapping = dict((n, i) for i, n in enumerate(G2.nodes))
    H = nx.relabel_nodes(G2, mapping)
    network = from_networkx(H, nx.spring_layout, scale=50, center=(0, 0))

    # Use node_renderer to attach hover tool
    network.node_renderer.glyph = Circle(size=10, fill_color=color_attr)
    network.node_renderer.hover_glyph = Circle(size=10, fill_color='white', line_width=2)
    network.node_renderer.selection_glyph = Circle(size=10, fill_color='white', line_width=2)

    # Customize the hover tool to filter by dta_org
    hover = HoverTool(
        tooltips=hover_vals,
        renderers=[network.node_renderer],  # Use node_renderer for hover tool
        mode='mouse'
    )

    x, y = zip(*network.layout_provider.graph_layout.values())
    node_labels = list(G2.nodes())
    src = ColumnDataSource({'x': x, 'y': y, 'name': [node_labels[i] for i in range(len(x))]})
    lbls = LabelSet(x='x', y='y', text='name', source=src, background_fill_color='white', text_font_size='10px', background_fill_alpha=.9)
    plot.renderers.append(lbls)

    # Add the hover tool to the plot
    plot.add_tools(hover)

    network.edge_renderer.glyph = MultiLine(line_alpha=0.3, line_width=1)
    network.edge_renderer.selection_glyph = MultiLine(line_color='black', line_width=2)
    network.edge_renderer.hover_glyph = MultiLine(line_color='black', line_width=2)

    network.selection_policy = NodesAndLinkedEdges()
    network.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(network)

    # # We want arrows in a directed graph illustrating the above data to go from commenter organization to discussion thread author
    # # organization (while either demonstrate inter-organizational collaboration, the commentor-thread author arrow direction indicates
    # # at the organization level which group was most informative/influential in maintaining the activity and overall health of the community itself)

    # # Use the unique_orgs list to populate all the nodes we'd want to connect

    # # Again use the nx library to created a directed graph (DiGraph) that we can then use to run PageRank/Gini coefficient analyses
    # # and generate other networked level metrics
    # G2 = nx.DiGraph()

    # # Create a dictionary that can be used to keep track of the number of connections from an organization to another
    # org_connection_count_dict = {}

    # # Iterate through autoware_network_diff_orgs to create a sample network
    # for index, row in commenter_DTA_gb_df.iterrows():
    #     commenter_org = row["commenter_organization"]
    #     dta_org = row["discussion_thread_author_organization"]

    #     commenter_dta_count = row['commenter_dta_connection_count']

    # if commenter_dta_count > 30:
    #     G2.add_edge(commenter_org, dta_org, weight=commenter_dta_count)
    #     org_connection_count_dict.update({(commenter_org, dta_org): commenter_dta_count})

    # # # To list the values of weights along each edge
    # # for src, tgt, data in G2.edges(data=True):
    # #     edge_weight = data['weight']
    # #     print(f"Edge from {src} to {tgt} has weight {edge_weight}")

    # # To print the names of all nodes
    # all_nodes = list(G2.nodes())

    # # Draw the graph
    # pos = nx.circular_layout(G2)
    # labels = {node: node for node in all_nodes}
    # plt.figure(figsize=(18, 20))  # Adjust the figure size as needed

    # nx.draw_networkx_nodes(G2, pos, node_size=400, node_color='skyblue')
    # nx.draw_networkx_labels(G2, pos, labels=labels, font_size=10, font_color='black')

    # # nx.draw(G2, pos, with_labels=True, labels=labels, node_size=1000, node_color='skyblue', font_size=10, font_color='black')

    # edge_labels = {(src, tgt): data['weight'] for src, tgt, data in G2.edges(data=True)}
    # nx.draw_networkx_edges(G2, pos)
    # nx.draw_networkx_edge_labels(G2, pos, edge_labels=edge_labels, font_size=8, font_color='red')

    # plt.title("Commenter-DTA Connection Network Across Organizations")
    # plt.show()

    # Convert the pandas DataFrame to a list of dictionaries
    response_list = commenter_DTA_gb_df.to_dict(orient="records")

    return JSONResponse(content={'plot_json': json_item(plot, "commenter_dta_connection_count_across_orgs"), 'response_list': response_list})
