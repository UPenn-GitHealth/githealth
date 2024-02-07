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


# Calculate issue data a single time:
# TODO: add some sort of timed caching method:
response_times: List[IssueResponseTime] = []
close_times: List[IssueCloseTime] = []


def get_response_times():
    global response_times
    if len(response_times) != 0:
        return response_times

    # TODO: Use database instead of CSV
    csv_dir = "Issues_Data/issues_data_v4.0"
    csv_pattern = os.path.join(csv_dir, "issues_*.csv")
    csv_files = glob.glob(csv_pattern)

    all_issues_data_list = []

    for file in csv_files:
        df = pd.read_csv(file)
        df["issues_created_at"] = pd.to_datetime(
            df["issues_created_at"], format="%Y-%m-%dT%H:%M:%SZ", errors="coerce"
        )
        df = df[~df["issues_created_at"].isnull()]
        df = df.dropna(subset=["issues_time_to_first_response"])
        df = df.drop_duplicates(subset=["issues_thread_id"])
        df["year"] = df["issues_created_at"].dt.year
        df["month"] = df["issues_created_at"].dt.month
        threshold_seconds = 5
        df = df[df["issues_time_to_first_response"] > threshold_seconds]

        if not df.empty:
            all_issues_data_list.append(df)

    if not all_issues_data_list:
        raise HTTPException(status_code=404, detail="No issues data found")

    all_issues_data = pd.concat(all_issues_data_list, ignore_index=True)
    all_issues_data["issues_time_to_first_response_hours"] = (
        all_issues_data["issues_time_to_first_response"] / 3600
    )

    sorted_issues_data = all_issues_data.sort_values(by=["year", "month"])
    response_data = sorted_issues_data[
        ["year", "month", "issues_time_to_first_response_hours"]
    ]

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
    csv_dir = "Issues_Data/issues_data_v4.0"
    csv_pattern = os.path.join(csv_dir, "issues_*.csv")
    csv_files = glob.glob(csv_pattern)

    all_issues_data_list = []

    for file in csv_files:
        df = pd.read_csv(file)
        df["issues_created_at"] = pd.to_datetime(
            df["issues_created_at"], format="%Y-%m-%dT%H:%M:%SZ", errors="coerce"
        )
        df = df[~df["issues_created_at"].isnull()]
        df = df.dropna(subset=["issues_time_to_close"])
        df = df.drop_duplicates(subset=["issues_thread_id"])
        df["year"] = df["issues_created_at"].dt.year
        df["month"] = df["issues_created_at"].dt.month
        threshold_seconds = 5
        df = df[df["issues_time_to_close"] > threshold_seconds]

        if not df.empty:
            all_issues_data_list.append(df)

    if not all_issues_data_list:
        raise HTTPException(status_code=404, detail="No issues data found")

    all_issues_data = pd.concat(all_issues_data_list, ignore_index=True)
    all_issues_data["issues_time_to_close_hours"] = (
        all_issues_data["issues_time_to_close"] / 3600
    )

    sorted_issues_data = all_issues_data.sort_values(by=["year", "month"])
    close_data = sorted_issues_data[["year", "month", "issues_time_to_close_hours"]]

    # Convert the pandas DataFrame to a list of dictionaries
    global close_times
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
    response_model=List[CommentCountByDiscussionThreadAuthor],
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
    gb_df_2 = gb_df_2[gb_df_2["comment_count"] > 5]

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
    response_list = gb_df_2.to_dict(orient="records")

    return response_list


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

    return response_list
