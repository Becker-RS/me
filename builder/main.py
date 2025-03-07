import os
import requests
from string import Template
from dateutil import parser

# Get environment variables
username = os.getenv('GITHUB_USERNAME')
token = os.getenv('GITHUB_TOKEN')

# Set up authenticated request
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

try:
    # Make GitHub API request with error handling
    response = requests.get(
        f"https://api.github.com/users/{username}",
        headers=headers
    )
    response.raise_for_status()  # Raise HTTP errors
    user = response.json()

except requests.exceptions.RequestException as e:
    print(f"API Error: {e}")
    # Fallback values if API fails
    user = {
        "name": "",
        "bio": "",
        "company": "",
        "location": "",
        "avatar_url": "",
        "html_url": f"https://github.com/{username}",
        "blog": "",
        "public_repos": 0,
        "followers": 0,
        "created_at": ""
    }

# Process user data with fallbacks
title = f'{user.get("name", "")} | GitHub Profile Page'.strip()
if not title:
    title = 'GitHub Profile Page'

company = f'@{user.get("company")}' if user.get("company") else ""
blog_url = f'https://{user.get("blog")}' if user.get("blog") else ""

d = {
    'username': username,
    'title': title, 
    'name': user.get('name', ''),
    'bio': user.get('bio', ''),
    'company': company,
    'location': user.get('location', ''),
    'avatar_url': user.get('avatar_url', ''),
    'github_url': user.get('html_url', f'https://github.com/{username}'),
    'blog_url': blog_url,
    'repos_url': f'{user.get("html_url", f"https://github.com/{username}")}?tab=repositories',
    'followers_url': f'{user.get("html_url", f"https://github.com/{username}")}?tab=followers',
    'repos_count': user.get('public_repos', 0),
    'followers_count': user.get('followers', 0),
    'created_at': (
        f'Since {parser.parse(user.get("created_at", "")).strftime("%B %Y")} on GitHub.' 
        if user.get("created_at") else "Since unknown date on GitHub."
    ),
}

# Generate HTML
with open('builder/template.html', 'r') as f:
    src = Template(f.read())
    result = src.safe_substitute(d)  # Use safe_substitute to prevent errors

with open('index.html', 'w') as f:
    f.write(result)

print("Profile was generated successfully")
