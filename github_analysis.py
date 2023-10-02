# import requests
from github import Github

access_token = "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"

# Create a PyGitHub client
g = Github(access_token)
repo_name = "autowarefoundation/autoware"
repo = g.get_repo(repo_name)

# Get repository details
print("Repository Name:", repo.name)
print("Description:", repo.description)
print("Stars:", repo.stargazers_count)
print("Forks:", repo.forks_count)

# Get issues
issues = repo.get_issues(state="all")  # state="all" includes open and closed issues
for issue in issues:
    print("Issue Title:", issue.title)
    print("State:", issue.state)
    print("Created At:", issue.created_at)
