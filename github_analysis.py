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
i = 0
# while i < 10:
for issue in issues:
    print("Start time:", issue.created_at)
    print("End time:", issue.closed_at) # if open, then closed_at is None
    print("Initiator:", issue.user.login)
    print("Repository:", issue.repository.name)
    print("Collaboration type:", issue.pull_request) #fixme
    print("Participants:", issue.assignees) #FIXME
    # get the people who participated on this issue, such as by commenting or being assigned
    #print("Participants:", issue.get_participants())
    print("Participants:", issue.get_comments())
    #extract the user id's from the comments
    for comment in issue.get_comments():
        print("commenter " + comment.user.login)
    print("Labels:", issue.labels)
    # print("Reviewers:", issue.requested_reviewers) #FIXME
    # extract who approved the request
    for reviewer in issue.get_review_requests():
        print("reviewer " + reviewer.user.login)
    print("PR Status: ", issue.state)
    print("URL: ", issue.url)
    break
