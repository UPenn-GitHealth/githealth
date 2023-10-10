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
    print("URL: ", issue.url)
    print("Repository:", issue.repository.name)
    print("Start time:", issue.created_at)
    print("End time:", issue.closed_at) # if open, then closed_at is None
    print("PR Status: ", issue.state)
    print("Initiator:", issue.user.login)
    print("Collaboration type:", issue.pull_request) #FIXME
    print("Assignees: ", issue.assignees) #FIXME
    commenters = set()
    #extract the user id's from the comments
    for comment in issue.get_comments():
        commenters.add(comment.user.login)
    print("Commenters: ", list(commenters))
    print("Labels: ", issue.labels)
    
    if issue.state == "closed":
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

    # break
