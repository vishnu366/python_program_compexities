import os
import subprocess
import json
import pandas as pd

# Path to the Python interpreter
python_executable = "C:/Users/vishn/AppData/Local/Microsoft/WindowsApps/python3.11.exe"

# Path to the directory containing the cloned projects
project_directory = 'C:/Users/vishn/project_rushitha/cloned_projects'

# Function to run Radon for MI and CC (returning numeric MI)
def run_radon(project_files):
    try:
        # Initialize total MI and file count
        total_mi_score = 0
        file_count = 0

        # Run Radon for Maintainability Index (MI)
        for file_path in project_files:
            mi_output = subprocess.run(
                [python_executable, '-m', 'radon', 'mi', '-j', file_path],
                capture_output=True,
                text=True
            )
            mi_data = json.loads(mi_output.stdout)

            # Extract MI score from each file
            for file, metrics in mi_data.items():
                mi_score = metrics.get('mi', None)
                if mi_score is not None:
                    total_mi_score += mi_score
                    file_count += 1

        # Calculate average MI if there are valid files
        avg_mi_score = round(total_mi_score / file_count, 2) if file_count > 0 else None

        # Run Radon for Cyclomatic Complexity (CC)
        cc_output = subprocess.run(
            [python_executable, '-m', 'radon', 'cc', '-s', project_files[0]],  # Only need to pass directory or 1 file
            capture_output=True,
            text=True
        )
        cc_data = cc_output.stdout.count('F')  # 'F' represents functions with high complexity

        return avg_mi_score, cc_data
    except Exception as e:
        print(f"Error running Radon for {project_files}: {e}")
        return None, None

# Function to get all Python files in the project
def get_python_files(project_path):
    py_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    return py_files

# Main analysis function
def analyze_project(project_path):
    # Get all .py files for radon analysis
    python_files = get_python_files(project_path)
    if python_files:
        radon_mi, radon_cc = run_radon(python_files)
    else:
        radon_mi, radon_cc = None, None

    return radon_mi, radon_cc

# List to store project results
project_data = []

# Loop through all projects and analyze them
for project in os.listdir(project_directory):
    project_path = os.path.join(project_directory, project)

    if os.path.isdir(project_path):
        print(f"Analyzing project: {project}")

        # Get analysis results from Radon
        radon_mi, radon_cc = analyze_project(project_path)

        # Append results to the project data
        project_data.append({
            'Project': project,
            'Radon MI (Numeric)': radon_mi,
            'Radon Cyclomatic Complexity': radon_cc
        })

# Convert the project data into a DataFrame and save it as a CSV file
df = pd.DataFrame(project_data)
df.to_csv('radon_analysis_results.csv', index=False)

print("Radon analysis complete. Results saved to 'radon_analysis_results.csv'")
