from github import Github
import yaml
import json
import csv
import re

REGEX = r"https://github.com/(?P<owner>[a-zA-Z0-9\-_.]+)/(?P<repo>[a-zA-Z0-9\-_.]+)\.git"

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

# Get repository details - we could add this to the main loop below but left out to not mess up data collection
for repo_name in repo_names:
    r = g.get_repo(repo_name)
    print("Repository Name:", r.name)
    print("Description:", r.description)
    print("API URL: ", r.url)
    print("HTML URL: ", r.html_url)
    print("Stars:", r.stargazers_count)
    print("Forks:", r.forks_count, "\n")

# open the file in the write mode
file = open('data.csv', 'w')

# create the csv writer
writer = csv.writer(file)

header = ['API URL', 'HTML URL', 'Repository', 'Start time', 'End time', 'PR Status', 'Initiator', 'Assignees', 'Commenters', 'Labels', 'Reviewers']

# write a row to the csv file
writer.writerow(header)

for repo_name in repo_names:
    r = g.get_repo(repo_name)
    # could make a new spreadsheet page here or something
    issues = r.get_issues(state="all")  # state="all" includes open and closed issues
    
    for issue in issues:
        # each one of these would be a line in the spreadsheet
        row = [issue.url, issue.html_url, issue.repository.name, issue.created_at, issue.closed_at, issue.state, issue.user.login]
        # print("API URL: ", issue.url)
        # print("HTML URL: ", issue.html_url) # goes to the webpage
        # print("Repository:", issue.repository.name)
        # print("Start time:", issue.created_at)
        # print("End time:", issue.closed_at) # if open, then closed_at is None
        # print("PR Status: ", issue.state)
        # print("Initiator:", issue.user.login)

        assignees = []
        for assignee in issue.assignees:
            assignees.append(assignee.login)

        row.append(assignees)

        # print("Assignees: ", assignees)

        commenters = set()
        for comment in issue.get_comments():
            commenters.add(comment.user.login)
        # print("Commenters: ", list(commenters))

        row.append(list(commenters))

        labels = []
        for label in issue.labels:
            labels.append(label.name)
        # print("Labels: ", labels)

        row.append(labels)

        reviewers_involved = set()
        
        if issue.state == "closed" and issue.pull_request is not None:

            for review in issue.as_pull_request().get_reviews():
                if review.user is not None:
                    reviewers_involved.add(review.user.login)

            # print("Reviewers: ", list(reviewers_involved))
        
        row.append(list(reviewers_involved))
        
        print("Row: ", row)
        writer.writerow(row)

# close the file
file.close()