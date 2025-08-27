import requests
import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  

def get_github_projects(username):
    """Fetch GitHub repositories for a user with authentication and forced GitHub Pages fallback"""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"GitHub API error: {response.status_code} - {response.text}")
        return []

    repos = response.json()
    projects = []

    for repo in repos:
        if repo.get('fork') or repo.get('size', 0) == 0:
            continue

        # Force fallback to GitHub Pages if homepage is missing
        if repo.get('homepage'):
            demo_url = repo['homepage']
        else:
            demo_url = f"https://{username}.github.io/{repo['name']}"

        projects.append({
            'title': repo['name'],
            'description': repo['description'] or 'No description',
            'tech_stack': ', '.join(repo.get('topics', [])),
            'github_url': repo['html_url'],
            'demo_url': demo_url
        })

    return projects
