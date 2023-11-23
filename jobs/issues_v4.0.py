# -*- coding: utf-8 -*-
"""issues_11_10_2023_submission

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XGEOX0ghghc3AC7fB24Zx1C2nz5WMHt2

Here's an explanation of each column in the issues_2023_new.csv file:

1. `issues_title`: Title of the GitHub issue. Each row represents an issue, and this column holds the title for each issue.

2. `issues_created_at`: Timestamp indicating when the GitHub issue was created.
issues_thread_id: Unique ID assigned to each GitHub issue. This ID helps in uniquely identifying and tracking each issue.

3. `issues_comment_id`: Unique ID assigned to each comment in the GitHub issue. If there are no comments (i.e., issues_no_of_comments is 0), this field would be an empty string for threads without comments and the original comment ID for comments and replies.

4. `issues_comment_type`: Indicates whether the comment is a top-level comment ("questioned") or a reply ("answered").

5. `issues_comment_text`: The text of the comment or reply.

6. `issues_comment_author`: User ID of the author who made the comment or reply.

7. `issues_time_to_close`: Time taken to close the GitHub issue in seconds. If the issue is not closed, this field would be None.

8. `issues_time_to_first_response`: Time taken for the first response in the GitHub issue in seconds. If there is no response, this field would be None.

9. `issues_no_of_comments`: Number of comments in the GitHub issue. If there are no comments, it would be 0.

10. `issues_commits`: Number of commits associated with a pull request (PR) linked to the issue. If the issue is not a PR, this field would be 0.

11. `issues_checks`: Number of checks (e.g., CI/CD checks) associated with a PR linked to the issue. If the issue is not a PR, this field would be 0.

12. `issues_files_changed`: Number of files changed in the PR linked to the issue. If the issue is not a PR, this field would be 0.

13. `issues_lines_changed`: Number of lines changed in the PR linked to the issue. If the issue is not a PR, this field would be 0.
"""

import requests
import csv
import pandas as pd
from datetime import datetime
import time  # Import the time module for rate limiting

# Replace with your GitHub personal access token
access_token = "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"

# GitHub API endpoint
base_url = "https://api.github.com"

# Repository details
owner = "autowarefoundation"
repo_name = "autoware"

# Define the year you want to filter discussions for
year = "2023"

# Initialize data containers
issues_data = []

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

# Function to fetch additional details for a pull request
def fetch_pull_request_details(pr_number):
    pr_details_url = f"{base_url}/repos/{owner}/{repo_name}/pulls/{pr_number}"
    response = requests.get(pr_details_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

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

# Fetch all issues (discussions)
page = 1
while True:
    params = {
        "state": "all",
        "per_page": 100,
        "page": page
    }
    response = requests.get(base_url + issues_endpoint, headers=headers, params=params)

    # Check for rate limit exceeded
    if response.status_code == 403:
        print(f"Rate limit exceeded. Waiting for {response.headers['Retry-After']} seconds.")
        time.sleep(int(response.headers['Retry-After']) + 1)  # Wait for the specified seconds
        continue

    if response.status_code == 200:
        issues = response.json()
        if not issues:
            break
        for issue in issues:
            # Extract the year part from the created_at timestamp
            created_at_year = issue["created_at"][:4]
            if created_at_year != year:
                continue  # Skip the issue if it's not in the specified year

            issue_data = {
                "issues_id": issue["id"],  # Save the original issue ID
                "issues_title": issue["title"],
                "issues_user_id": issue["user"]["login"],
                "issues_created_at": issue["created_at"],
                "issues_comments": fetch_comments(issue["number"]),
                "issues_time_to_close": calculate_time_to_close(issue),
                "issues_time_to_first_response": calculate_time_to_first_response(issue),
                "issues_no_of_comments": len(fetch_comments(issue["number"]))  # New column: number of comments
            }

            # Fetch additional details for PRs
            if "pull_request" in issue:
                pr_details = fetch_pull_request_details(issue["number"])
                if pr_details:
                    issue_data["issues_commits"] = pr_details.get("commits", 0)
                    issue_data["issues_checks"] = pr_details.get("check_runs_count", 0)
                    issue_data["issues_files_changed"] = pr_details.get("changed_files", 0)
                    issue_data["issues_lines_changed"] = pr_details.get("additions", 0) + pr_details.get("deletions", 0)

            issues_data.append(issue_data)
        page += 1
    else:
        print(f"Failed to fetch issues. Status code: {response.status_code}")
        break

# Create a new data structure with the desired format
new_data = []

for discussion in issues_data:
    thread_id = discussion["issues_id"]  # Use the original issue ID as thread_id
    thread_creator = discussion["issues_user_id"]  # Get the thread creator's username

    # Create a placeholder for threads without comments
    if not discussion["issues_comments"]:
        comment_data = {
            "issues_title": discussion["issues_title"],  # Include the title
            "issues_created_at": discussion["issues_created_at"],
            "issues_thread_id": thread_id,
            "issues_comment_id": "",  # Empty for threads without comments
            "issues_comment_type": "",  # Empty for threads without comments
            "issues_comment_text": "",  # Empty for threads without comments
            "issues_comment_author": thread_creator,  # Include the thread creator
            "issues_time_to_close": None,
            "issues_time_to_first_response": None,
            "issues_no_of_comments": discussion["issues_no_of_comments"],  # Include the number of comments
            "issues_commits": discussion.get("issues_commits", 0),  # Include number of commits
            "issues_checks": discussion.get("issues_checks", 0),  # Include number of checks
            "issues_files_changed": discussion.get("issues_files_changed", 0),  # Include number of files changed
            "issues_lines_changed": discussion.get("issues_lines_changed", 0),  # Include number of lines changed
        }
        new_data.append(comment_data)
    else:
        time_to_close = None
        time_to_first_response = None
        # Calculate time to close and time to first response
        comment_dates = [datetime.strptime(comment["created_at"], "%Y-%m-%dT%H:%M:%SZ") for comment in discussion["issues_comments"]]
        if discussion["issues_time_to_close"]:
            time_to_close = discussion["issues_time_to_close"]
        if discussion["issues_time_to_first_response"]:
            time_to_first_response = discussion["issues_time_to_first_response"]
        for index, comment in enumerate(discussion["issues_comments"], start=1):
            comment_creator = comment["user"]["login"]
            if comment_creator == thread_creator:
                comment_type = "questioned"
            else:
                comment_type = "answered"

            comment_data = {
                "issues_title": discussion["issues_title"],  # Include the title
                "issues_created_at": comment["created_at"],
                "issues_thread_id": thread_id,
                "issues_comment_id": comment["id"],  # Use the original comment ID as subtitle_id
                "issues_comment_type": comment_type,
                "issues_comment_text": comment["body"],
                "issues_comment_author": comment_creator,  # Include the comment creator
                "issues_time_to_close": time_to_close,
                "issues_time_to_first_response": time_to_first_response,
                "issues_no_of_comments": discussion["issues_no_of_comments"],  # Include the number of comments
                "issues_commits": discussion.get("issues_commits", 0),  # Include number of commits
                "issues_checks": discussion.get("issues_checks", 0),  # Include number of checks
                "issues_files_changed": discussion.get("issues_files_changed", 0),  # Include number of files changed
                "issues_lines_changed": discussion.get("issues_lines_changed", 0),  # Include number of lines changed
            }
            new_data.append(comment_data)

            # Include replies as well
            replies = fetch_comments(comment["id"])
            for reply in replies:
                reply_creator = reply["user"]["login"]
                reply_type = "answered"

                reply_data = {
                    "issues_title": discussion["issues_title"],  # Include the title
                    "issues_created_at": reply["created_at"],
                    "issues_thread_id": thread_id,
                    "issues_comment_id": reply["id"],  # Use the original reply ID as subtitle_id
                    "issues_comment_type": reply_type,
                    "issues_comment_text": reply["body"],
                    "issues_comment_author": reply_creator,  # Include the reply creator
                    "issues_time_to_close": time_to_close,
                    "issues_time_to_first_response": time_to_first_response,
                    "issues_no_of_comments": discussion["issues_no_of_comments"],  # Include the number of comments
                    "issues_commits": discussion.get("issues_commits", 0),  # Include number of commits
                    "issues_checks": discussion.get("issues_checks", 0),  # Include number of checks
                    "issues_files_changed": discussion.get("issues_files_changed", 0),  # Include number of files changed
                    "issues_lines_changed": discussion.get("issues_lines_changed", 0),  # Include number of lines changed
                }
                new_data.append(reply_data)

# Create a CSV file with the new data structure
csv_file_path = f"issues_{year}_new.csv"
with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
    fieldnames = [
        "issues_title", "issues_created_at", "issues_thread_id", "issues_comment_id",
        "issues_comment_type", "issues_comment_text", "issues_comment_author",
        "issues_time_to_close", "issues_time_to_first_response", "issues_no_of_comments",
        "issues_commits", "issues_checks", "issues_files_changed", "issues_lines_changed"
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for data in new_data:
        writer.writerow(data)

# Read the new CSV file into a DataFrame
issues_new_df = pd.read_csv(csv_file_path)

# Display the first 5 rows of the new DataFrame
print(issues_new_df.head(5))

# Display information about the new DataFrame
print(issues_new_df.info())

print(f"Data analysis and manipulation completed. New data saved to {csv_file_path}")
