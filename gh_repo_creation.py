# This file will be used to create new GitHub repositories using the PyGithub library

from github import Github

# Second, initialize a Github object using a personal access token
personal_access_token = "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"
g = Github(personal_access_token)

user = g.get_user()
print(f"User name: {user.name}")
print(f"User login: {user.login}")

# Store all repos in a list
repos = []

# Third, create a set of 10 new repositories associated with this account
for i in range(1, 11):
    repo = user.create_repo("githealth-test-repo-" + str(i))
    repos.append(repo)
    print("Created repository " + str(i))

# Finally, print out the URLs of all the repositories created
for repo in repos:
    print(repo.clone_url)