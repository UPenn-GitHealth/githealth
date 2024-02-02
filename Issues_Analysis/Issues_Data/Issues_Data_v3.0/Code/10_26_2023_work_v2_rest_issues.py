# -*- coding: utf-8 -*-
"""10_26_2023_work_v2 - REST Issues

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EzE8dnE0vvvPB50mUaulz-jtDMvfCGwC
"""

import requests
import csv
import json
import pandas as pd
import numpy as np

# Replace with your GitHub personal access token
access_token = "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"

# GitHub API endpoint
base_url = "https://api.github.com"

# Repository details
owner = "autowarefoundation"
repo_name = "autoware"

# Define the year you want to filter discussions for
year = "2014"

# Initialize data containers
discussions_data = []

# Prepare headers with authorization
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Define the API endpoint for issues in the repository
issues_endpoint = f"/repos/{owner}/{repo_name}/issues"

# Function to fetch comments for an issue
def fetch_comments(issue_number):
    comments_url = f"{base_url}{issues_endpoint}/{issue_number}/comments"
    response = requests.get(comments_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

# Function to calculate the time to close an issue
def calculate_time_to_close(issue):
    if "closed_at" in issue and "created_at" in issue and issue["closed_at"] is not None and issue["created_at"] is not None:
        closed_at = datetime.strptime(issue["closed_at"], "%Y-%m-%dT%H:%M:%SZ")
        created_at = datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        return (closed_at - created_at).total_seconds()
    return None

# Function to calculate the time to the first response in seconds
def calculate_time_to_first_response(issue):
    created_at = datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    comments = fetch_comments(issue["number"])
    if comments:
        first_comment = min(comments, key=lambda x: datetime.strptime(x["created_at"], "%Y-%m-%dT%H:%M:%SZ"))
        first_response_at = datetime.strptime(first_comment["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        return (first_response_at - created_at).total_seconds()
    return None

# Function to categorize issues as "Bugs" or "Improvements"
def categorize_issue(issue):
    labels = issue.get("labels", [])
    for label in labels:
        if label["name"].lower() == "bug":
            return "Bug"
        elif label["name"].lower() == "improvement":
            return "Improvement"
    return "Other"

# Fetch all issues (discussions)
page = 1
while True:
    params = {
        "state": "all",
        "per_page": 100,
        "page": page
    }
    response = requests.get(base_url + issues_endpoint, headers=headers, params=params)
    if response.status_code == 200:
        issues = response.json()
        if not issues:
            break
        for issue in issues:
            # Check if the issue was created in the specified year
            created_at = issue.get("created_at", "")[:4]  # Extract the year part
            if created_at == year:
                discussion_data = {
                    "title": issue["title"],
                    "user_id": issue["user"]["login"],
                    "created_at": issue.get("created_at", ""),
                    "comments": fetch_comments(issue["number"]),
                    "time_to_close": calculate_time_to_close(issue),
                    "issue_category": categorize_issue(issue),
                    "time_to_first_response": calculate_time_to_first_response(issue)
                }
                discussions_data.append(discussion_data)
        page += 1
    else:
        print(f"Failed to fetch issues. Status code: {response.status_code}")
        break

# Calculate mean issue age
issue_age_seconds = [issue["time_to_close"] for issue in discussions_data if issue["time_to_close"] is not None]
mean_issue_age = sum(issue_age_seconds) / len(issue_age_seconds) if issue_age_seconds else None

# Calculate mean time to first response
time_to_first_response_seconds = [issue["time_to_first_response"] for issue in discussions_data if issue["time_to_first_response"] is not None]
mean_time_to_first_response = sum(time_to_first_response_seconds) / len(time_to_first_response_seconds) if time_to_first_response_seconds else None

# Calculate mean time to close
time_to_close_seconds = [issue["time_to_close"] for issue in discussions_data if issue["time_to_close"] is not None]
mean_time_to_close = sum(time_to_close_seconds) / len(time_to_close_seconds) if time_to_close_seconds else None

# Create a new data structure with the desired format
new_data = []

for discussion in discussions_data:
    thread_id = len(new_data) + 1  # Assign unique thread ID
    thread_creator = discussion["user_id"]  # Get the thread creator's username

    # Create a placeholder for threads without comments
    if not discussion["comments"]:
        comment_data = {
            "title": discussion["title"],  # Include the title
            "Created_at": discussion["created_at"],
            "thread_id": thread_id,
            "subtitle_id": "",  # Empty for threads without comments
            "Type": "",  # Empty for threads without comments
            "Comment_text": "",  # Empty for threads without comments
            "Time_to_Close": None,
            "Time_to_First_Response": None,
        }
        new_data.append(comment_data)
    else:
        time_to_close = None
        time_to_first_response = None
        # Calculate time to close and time to first response
        comment_dates = [datetime.strptime(comment["created_at"], "%Y-%m-%dT%H:%M:%SZ") for comment in discussion["comments"]]
        if discussion["time_to_close"]:
            time_to_close = discussion["time_to_close"]
        if discussion["time_to_first_response"]:
            time_to_first_response = discussion["time_to_first_response"]
        for index, comment in enumerate(discussion["comments"], start=1):
            comment_creator = comment["user"]["login"]
            if comment_creator == thread_creator:
                comment_type = "questioned"
            else:
                comment_type = "answered"

            comment_data = {
                "title": discussion["title"],  # Include the title
                "Created_at": comment["created_at"],
                "thread_id": thread_id,
                "subtitle_id": index,  # Assign unique subtitle ID
                "Type": comment_type,
                "Comment_text": comment["body"],
                "Time_to_Close": time_to_close,
                "Time_to_First_Response": time_to_first_response,
            }
            new_data.append(comment_data)

# Create a CSV file with the new data structure
csv_file_path = f"discussions_{year}_new.csv"
with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
    fieldnames = ["title", "Created_at", "thread_id", "subtitle_id", "Type", "Comment_text", "Time_to_Close", "Time_to_First_Response"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for data in new_data:
        writer.writerow(data)

# Load the CSV data into a Pandas DataFrame for analysis
discussion_summary_df = pd.read_csv(csv_file_path)

# Calculate the mean issue age, mean time to close, and mean time to first response
print("Mean Issue Age (in seconds):", mean_issue_age)
print("Mean Time to Close (in seconds):", mean_time_to_close)
print("Mean Time to First Response (in seconds):", mean_time_to_first_response)

# Display the DataFrame to check the data
print(discussion_summary_df)