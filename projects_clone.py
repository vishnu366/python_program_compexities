import os
import shutil
import pandas as pd
import subprocess

# Step 1: Load the CSV file with project information
csv_file = './github_projects_with_domains.csv'  # Update this path to your CSV file
df = pd.read_csv(csv_file)

# Step 2: Define the directory where you want to clone the projects
clone_directory = './cloned_projects'  # Update this path to the desired location

# Helper function to handle permission errors
def handle_remove_readonly(func, path, exc_info):
    import stat
    os.chmod(path, stat.S_IWRITE)
    func(path)

# Step 3: Delete the directory if it exists and create a new one
if os.path.exists(clone_directory):
    print(f"Deleting existing directory: {clone_directory}")
    shutil.rmtree(clone_directory, onerror=handle_remove_readonly)  # Use onerror to handle permissions

print(f"Creating new directory: {clone_directory}")
os.makedirs(clone_directory)  # Create a new empty directory

# Step 4: Clone each repository from the 'url' column
for index, row in df.iterrows():
    repo_url = row['url']  # Extract the repository URL
    repo_name = row['Project']  # Extract the project name for naming the folder
    
    # Define the path where the repository will be cloned
    repo_path = os.path.join(clone_directory, repo_name)

    # Clone the repository
    print(f"Cloning {repo_name} from {repo_url}...")
    subprocess.run(['git', 'clone', repo_url, repo_path])

print("Cloning process completed.")
