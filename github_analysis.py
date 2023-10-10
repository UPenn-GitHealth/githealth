from github import Github
import yaml

access_token = "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"

def get_repos(g):
    repo_name = "autowarefoundation/autoware"
    file_path = "autoware.repos"

    try:
        repo = g.get_repo(repo_name)
        file_content = repo.get_contents(file_path).decoded_content.decode("utf-8")
        
        # Parse the YAML con
        parsed_content = yaml.safe_load(file_content)

        # Extract repository details
        repositories = []
        for repo_key, repo_details in parsed_content['repositories'].items():
            repo_name = "/".join(repo_details['url'].split('/')[-2:])
            repositories.append(g.get_repo(repo_name))
        return repositories
    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return []

# Create a PyGitHub client
g = Github(access_token)
repos = get_repos(g)

# Get repository details
for r in repos:
    print("Repository Name:", r.name)
    print("Description:", r.description)
    print("Stars:", r.stargazers_count)
    print("Forks:", r.forks_count)
    print("\n")


# Get issues
# issues = repo.get_issues(state="all")  # state="all" includes open and closed issues
# for issue in issues:
#     print("Issue Title:", issue.title)
#     print("State:", issue.state)
#     print("Created At:", issue.created_at)


# below is Anshul's garbage
# Get issues
# issues = repo.get_issues(state="all")  # state="all" includes open and closed issues
# i = 0
# # while i < 10:
# for issue in issues:
#     print("Start time:", issue.created_at)
#     print("End time:", issue.closed_at) # if open, then closed_at is None
#     print("Initiator:", issue.user.login)
#     print("Repository:", issue.repository.name)
#     print("Collaboration type:", issue.pull_request) #fixme
#     print("Participants:", issue.assignees) #FIXME
#     # get the people who participated on this issue, such as by commenting or being assigned
#     #print("Participants:", issue.get_participants())
#     print("Participants:", issue.get_comments())
#     #extract the user id's from the comments
#     for comment in issue.get_comments():
#         print("commenter " + comment.user.login)
#     print("Labels:", issue.labels)
#     # print("Reviewers:", issue.requested_reviewers) #FIXME
#     # extract who approved the request
#     for reviewer in issue.get_review_requests():
#         print("reviewer " + reviewer.user.login)
#     print("PR Status: ", issue.state)
#     print("URL: ", issue.url)
#     break

