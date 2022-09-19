from service.githubAPI2 import GithubClient, GithubRepo

token = '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'

github_client = GithubClient(token=token)
url = github_client.fetch_repo_archive_url('django/django')
repo = GithubRepo(archive_url=url, token=token)
