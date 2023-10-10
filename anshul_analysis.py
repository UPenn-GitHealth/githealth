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
    print("API URL: ", issue.url)
    print("HTML URL: ", issue.html_url) # goes to the webpage
    print("Repository:", issue.repository.name)
    print("Start time:", issue.created_at)
    print("End time:", issue.closed_at) # if open, then closed_at is None
    print("PR Status: ", issue.state)
    print("Initiator:", issue.user.login)
    print("Collaboration type: Issue") #FIXME

    assignees = []
    for assignee in issue.assignees:
        assignees.append(assignee.login)

    print("Assignees: ", assignees)

    commenters = set()
    for comment in issue.get_comments():
        commenters.add(comment.user.login)
    print("Commenters: ", list(commenters))

    labels = []
    for label in issue.labels:
        labels.append(label.name)
    print("Labels: ", labels)
    
    if issue.state == "closed" and issue.pull_request is not None:
        reviewers_involved = set()

        for review in issue.as_pull_request().get_reviews():
            reviewers_involved.add(review.user.login)

        print("Reviewers that reviewed: ", list(reviewers_involved))

        users_requested, teams_requested = issue.as_pull_request().get_review_requests()

        for user in users_requested:
            reviewers_involved.add(user.login)

        for team in teams_requested:
            for user in team.get_members():
                reviewers_involved.add(user.login)

        reviewers_involved = list(reviewers_involved)
        print("All invited reviewers: ", reviewers_involved)

# do the same for pull requests

# pull_requests = repo.get_pulls(state="all")

# for pull_request in pull_requests:
#     print("API URL: ", pull_request.url)
#     print("HTML URL: ", pull_request.html_url) # goes to the webpage
#     print("Repository:", pull_request.as_issue().repository.name)
#     print("Start time:", pull_request.created_at)
#     print("End time:", pull_request.closed_at) # if open, then closed_at is None
#     print("PR Status: ", pull_request.state)
#     print("Initiator:", pull_request.user.login)
#     print("Collaboration type: Pull Request") #FIXME

#     assignees = []
#     for assignee in pull_request.assignees:
#         assignees.append(assignee.login)

#     print("Assignees: ", assignees)

#     commenters = set()
#     for comment in pull_request.get_comments():
#         commenters.add(comment.user.login)
#     print("Commenters: ", list(commenters))

#     labels = []
#     for label in pull_request.labels:
#         labels.append(label.name)
#     print("Labels: ", labels)
    
#     if pull_request.state == "closed":
#         reviewers_involved = set()

#         for review in pull_request.get_reviews():
#             reviewers_involved.add(review.user.login)

#         print("Reviewers that reviewed: ", list(reviewers_involved))

#         users_requested, teams_requested = pull_request.get_review_requests()

#         for user in users_requested:
#             reviewers_involved.add(user.login)

#         for team in teams_requested:
#             for user in team.get_members():
#                 reviewers_involved.add(user.login)

#         reviewers_involved = list(reviewers_involved)
#         print("All invited reviewers: ", reviewers_involved)
