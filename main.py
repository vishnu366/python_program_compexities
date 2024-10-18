from github import Github
import os
import pandas as pd
from datetime import datetime

# GitHub Access Token (Make sure you create one at https://github.com/settings/tokens)
ACCESS_TOKEN = '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'

# Initialize Github instance
g = Github(ACCESS_TOKEN)

# Define new categories based on size (in KB)
categories = {
    "Small": {"min": 0, "max": 1024},         # <= 512 KB
    "Medium": {"min": 1024, "max": 2048},     # > 512 KB and <= 1MB
    "Large": {"min": 2048, "max": 3072},     # > 1MB and <= 1536 KB
}

# Function to categorize the project based on size
def categorize_project(size_in_kb):
    for category, size_range in categories.items():
        if size_range['min'] <= size_in_kb <= size_range['max']:
            return category
    return None

# Function to calculate the age of the project in days
def calculate_project_age(creation_date):
    creation_datetime = datetime.strptime(creation_date, '%Y-%m-%dT%H:%M:%SZ')
    current_datetime = datetime.now()
    age_in_days = (current_datetime - creation_datetime).days
    return age_in_days

# Function to fetch project data including project domain
def fetch_project_data(repo):
    project_info = {}
    project_info['Project'] = repo.name
    project_info['url'] = repo.html_url
    project_info['size_in_kb'] = repo.size  # GitHub size is in KB
    project_info['stargazers_count'] = repo.stargazers_count
    project_info['forks_count'] = repo.forks_count
    project_info['watchers_count'] = repo.watchers_count
    project_info['open_issues_count'] = repo.open_issues_count
    project_info['age_in_days'] = calculate_project_age(repo.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'))  # Project age in days

    # Extract domain information from topics or description
    project_info['topics'] = ', '.join(repo.get_topics())  # GitHub API provides topics as a list
    project_info['description'] = repo.description or 'No description provided'
    
    # Determine project domain based on topics or description (simple heuristic)
    if 'machine-learning' in project_info['topics'] or 'AI' in project_info['description'].lower():
        project_info['domain'] = 'Machine Learning/AI'
    elif 'web' in project_info['topics'] or 'web' in project_info['description'].lower():
        project_info['domain'] = 'Web Development'
    elif 'data' in project_info['topics'] or 'data' in project_info['description'].lower():
        project_info['domain'] = 'Data Science'
    else:
        project_info['domain'] = 'General'

    return project_info

# List to store all projects
project_data = []

# Search for Python repositories
repositories = g.search_repositories(query='language:python', sort='stars', order='desc')

# Counters for each category
category_counts = {"Small": 0, "Medium": 0, "Large": 0}
category_limits = 10  # We now want 10 projects per category

# Loop through repositories and collect data
for repo in repositories:
    size_in_kb = repo.size  # GitHub API returns size in KB
    category = categorize_project(size_in_kb)

    if category and category_counts[category] < category_limits:
        project_info = fetch_project_data(repo)
        project_info['category'] = category  # Add the category to the project data
        project_data.append(project_info)
        category_counts[category] += 1

    # Stop if we have enough projects in each category
    if all(count >= category_limits for count in category_counts.values()):
        break

# Convert project data to a DataFrame
df = pd.DataFrame(project_data)

# Save the data to a CSV file
csv_file_path = os.path.join(os.getcwd(), 'github_projects_with_domains.csv')
df.to_csv(csv_file_path, index=False)

print(f"Project data saved to {csv_file_path}")
