# -*- coding: utf-8 -*-
"""Discussions_11_10_v4_submission

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13qxj9uz8IFtyTlW1M87Q3yZXtktiiQmk

Here's an explanation of each column in the `final_github_discussion_data.csv` file:

1. `discussion_title`: Title of the discussion thread. Each row represents a discussion thread, and this column holds the title for each thread
2. `discussion_thread_id`: Unique ID assigned to each discussion thread. This ID helps in uniquely identifying and tracking each discussion thread.
3. `discussion_thread_created_at`: Timestamp indicating when the discussion thread was created.
4. `discussion_thread_author_id`: User ID of the creator of the discussion thread.
5. `discussion_thread_comment_count`: Number of comments in the discussion thread. If there are no comments, it would be 0.
6. `discussion_answered_or_unanswered`: Indicates whether the discussion thread is answered or unanswered. If discussion_thread_comment_count is 0, it is considered unanswered.
7. `discussion_comment_id`: Unique ID assigned to each comment in the discussion thread. If there are no comments (i.e., discussion_thread_comment_count is 0), this field would be NaN. If there are subthreads, it will say "combined_text."
8. `discussion_parent_comment_id`: Records the comment ID for each sub-comment. If a comment is a top-level comment, this field would be NaN.
9. `discussion_comment_created_at`: Timestamp indicating when a comment or reply was created.
10. `discussion_comment_author`: User ID of the author who made the comment or reply.
11. `discussion_comment_text`: The text of the comment or reply.
"""

import requests
import csv
import pandas as pd

# Replace with your GitHub personal access token
access_token = "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"

# GitHub API endpoint
base_url = "https://api.github.com/graphql"

# Repository details
owner = "autowarefoundation"
repo_name = "autoware"

# Define the GraphQL query to retrieve discussions with pagination
graphql_query = """
# GraphQL Query to Retrieve Discussions with Pagination

{
  # Specify the repository by providing the owner and name
  repository(owner: "%s", name: "%s") {

    # Retrieve discussions from the repository
    discussions(
      # Limit the number of discussions to 100
      first: 100,

      # Order discussions by creation timestamp in ascending order
      orderBy: { field: CREATED_AT, direction: ASC },

      # Start pagination from the beginning
      after: null
    ) {

      # Retrieve information about discussions as edges
      edges {

        # Access the node representing a discussion
        node {

          # Unique identifier for the discussion
          id

          # Title of the discussion
          title

          # Timestamp when the discussion was created
          createdAt

          # Author information for the discussion
          author {
            login  # GitHub login ID of the author
          }

          # Retrieve comments associated with the discussion
          comments(
            # Limit the number of comments to 10
            first: 10
          ) {

            # Total count of comments
            totalCount

            # Access individual comment nodes as edges
            edges {

              # Access the node representing a comment
              node {

                # Unique identifier for the comment
                id

                # Author information for the comment
                author {
                  login  # GitHub login ID of the author
                }

                # Body text of the comment
                body

                # Timestamp when the comment was created
                createdAt

                # Retrieve replies associated with the comment
                replies(
                  # Limit the number of replies to 10
                  first: 10
                ) {

                  # Access individual reply nodes as edges
                  edges {

                    # Access the node representing a reply
                    node {

                      # Unique identifier for the reply
                      id

                      # Author information for the reply
                      author {
                        login  # GitHub login ID of the author
                      }

                      # Body text of the reply
                      body

                      # Timestamp when the reply was created
                      createdAt
                    }
                  }
                }
              }
            }
          }
        }
      }

      # Information about pagination
      pageInfo {

        # Indicates if there is a next page
        hasNextPage

        # Cursor pointing to the end of the current page
        endCursor
      }
    }
  }
}
""" % (owner, repo_name)

# Define headers with authorization
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Initialize a list for collecting discussion data
discussion_data = []

# Use pagination to retrieve all discussion data
while True:
    # Make a POST request to the GitHub API with the GraphQL query
    response = requests.post(base_url, json={"query": graphql_query}, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()

        # Extract repository and discussions information from the response
        repository = data["data"]["repository"]
        discussions = repository["discussions"]
        edges = discussions["edges"]

        # Iterate over discussion threads
        for edge in edges:
            discussion = edge["node"]
            discussion_id = discussion["id"]
            title = discussion["title"]
            created_at = discussion["createdAt"]
            author = discussion["author"]["login"] if discussion["author"] else "Unknown"
            num_comments = discussion["comments"]["totalCount"]
            answered_unanswered = "Answered" if num_comments > 0 else "Unanswered"

            # Append data for discussions
            discussion_data.append([
                title,
                discussion_id,
                created_at,
                author,
                num_comments,
                answered_unanswered,
                None,
                None,
                None,
                None,
                None  # Add None for comment_created_at
            ])

            # If there are comments in the discussion thread, iterate over comments
            if num_comments > 0:
                for comment in discussion["comments"]["edges"]:
                    comment_node = comment["node"]
                    comment_id = comment_node["id"]
                    comment_author = comment_node["author"]["login"] if comment_node.get("author") else "Unknown"
                    comment_text = comment_node["body"]
                    comment_created_at = comment_node.get("createdAt", None)
                    if comment_created_at:
                        comment_created_at = pd.to_datetime(comment_created_at)

                    # Append data for comments
                    discussion_data.append([
                        title,
                        discussion_id,
                        created_at,
                        author,
                        num_comments,
                        answered_unanswered,
                        comment_id,
                        comment_author,
                        comment_text,
                        None,  # Add None for parent_id
                        comment_created_at  # Add comment_created_at for comment
                    ])

                    # If there are replies to the comment, iterate over replies (sub-comments)
                    if "replies" in comment_node:
                        for reply in comment_node["replies"]["edges"]:
                            reply_node = reply["node"]
                            reply_id = reply_node["id"]
                            reply_author = reply_node["author"]["login"] if reply_node.get("author") else "Unknown"
                            reply_text = reply_node["body"]
                            reply_created_at = reply_node.get("createdAt", None)
                            if reply_created_at:
                                reply_created_at = pd.to_datetime(reply_created_at)

                            # Append data for replies (sub-comments)
                            discussion_data.append([
                                title,
                                discussion_id,
                                created_at,
                                author,
                                num_comments,
                                answered_unanswered,
                                reply_id,
                                reply_author,
                                reply_text,
                                comment_id,  # Set parent_id to the comment_id
                                reply_created_at  # Add reply_created_at for reply
                            ])

        # Extract page information for pagination
        page_info = discussions["pageInfo"]

        # Check if there is a next page, and update the GraphQL query for pagination
        if page_info["hasNextPage"]:
            graphql_query = """
            {
              repository(owner: "%s", name: "%s") {
                discussions(first: 100, orderBy: {field: CREATED_AT, direction: ASC}, after: "%s") {
                  edges {
                    node {
                      id
                      title
                      createdAt
                      author {
                        login
                      }
                      comments(first: 10) {
                        totalCount
                        edges {
                          node {
                            id
                            author {
                              login
                            }
                            body
                            replies(first: 10) {
                              edges {
                                node {
                                  id
                                  author {
                                    login
                                  }
                                  body
                                  createdAt  # Include createdAt for replies
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                  pageInfo {
                    hasNextPage
                    endCursor
                  }
                }
              }
            }
            """ % (owner, repo_name, page_info["endCursor"])
        else:
            break
    else:
        # Print an error message if the request fails
        print("Failed to retrieve discussions. Status code:", response.status_code)
        print(response.text)
        break

# Save the discussion data to a CSV file
with open('github_discussion_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Title", "Discussion ID", "Created At", "User ID", "Comment Count", "Answered/Unanswered", "Comment ID", "Comment Author", "Comment Text", "Parent ID", "Comment Created At"])
    csv_writer.writerows(discussion_data)

# Read the CSV file into a DataFrame
discussion_df = pd.read_csv('github_discussion_data.csv')

# Filter rows based on conditions
filtered_df = discussion_df[~((discussion_df["Comment Count"] > 0) & (discussion_df["Answered/Unanswered"] == "Answered") & discussion_df["Comment ID"].isnull() & discussion_df["Comment Author"].isnull() & discussion_df["Comment Text"].isnull() & discussion_df["Parent ID"].isnull() & discussion_df["Comment Created At"].isnull())]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('filtered_github_discussion_data.csv', index=False)

# Display DataFrame information
filtered_df.info()

# Rename columns
filtered_df = filtered_df.rename(columns={
    'Title': 'discussion_title',
    'Discussion ID': 'discussion_thread_id',
    'Created At': 'discussion_thread_created_at',
    'User ID': 'discussion_thread_author_id',
    'Comment Count': 'discussion_thread_comment_count',
    'Answered/Unanswered': 'discussion_answered_or_unanswered',
    'Comment ID': 'discussion_comment_id',
    'Comment Author': 'discussion_comment_author',
    'Comment Text': 'discussion_comment_text',
    'Parent ID': 'discussion_parent_comment_id',
    'Comment Created At': 'discussion_comment_created_at'
})

# Save the DataFrame with the updated column names to a new CSV file
filtered_df.to_csv('filtered_github_discussion_data_updated.csv', index=False)

# Save the filtered DataFrame to a new CSV file
updated_df = pd.read_csv('filtered_github_discussion_data_updated.csv')

# Display DataFrame information
updated_df.info()

# Reorder columns
column_sequence = [
    'discussion_title',
    'discussion_thread_id',
    'discussion_thread_created_at',
    'discussion_thread_author_id',
    'discussion_thread_comment_count',
    'discussion_answered_or_unanswered',
    'discussion_comment_id',
    'discussion_parent_comment_id',
    'discussion_comment_created_at',
    'discussion_comment_author',
    'discussion_comment_text'
]

# Reorder columns and save to a new CSV file
updated_df = updated_df[column_sequence]
updated_df.to_csv('final_github_discussion_data.csv', index=False)

# Display DataFrame information
updated_df.info()