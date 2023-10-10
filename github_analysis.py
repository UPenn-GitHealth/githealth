from github import Github
import yaml
import json
import re

REGEX = r"https://github.com/(?P<owner>[a-zA-Z0-9\-_]+)/(?P<repo>[a-zA-Z0-9\-_]+)\.git"

access_token = "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"

def get_repos(g):
    repo_name = "autowarefoundation/autoware"
    file_path = "autoware.repos"

    try:
        repo = g.get_repo(repo_name)
        file_content = repo.get_contents(file_path).decoded_content.decode("utf-8")
        
        # Parse the YAML content
        parsed_content = yaml.safe_load(file_content)

        repository_names = []

        for repo_key, repo_details in parsed_content['repositories'].items():
            url = repo_details['url']
            print(url)
            matches = re.search(REGEX, url)
            if matches:
                owner = matches.group('owner')
                repo = matches.group('repo')

                repository_names.append(f"{owner}/{repo}")

        return repository_names

    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return []


# Create a PyGitHub client
g = Github(access_token)
repo_names = get_repos(g)

# Get repository details
for repo_name in repo_names:
    r = g.get_repo(repo_name)
    print("Repository Name:", r.name)
    print("Description:", r.description)
    print("Stars:", r.stargazers_count)
    print("Forks:", r.forks_count)
    print("\n")

for repo_name in repo_names:
    r = g.get_repo(repo_name)
    # could make a new spreadsheet page here or something
    issues = r.get_issues(state="all")  # state="all" includes open and closed issues
    for issue in issues:
        # each one of these would be a line in the spreadsheet
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
