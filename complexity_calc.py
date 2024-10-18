import os
import subprocess
import math
import pandas as pd
import re

# Path to the Python interpreter
python_executable = "C:/Users/vishn/AppData/Local/Microsoft/WindowsApps/python3.11.exe"

# Define the path to the directory containing the cloned projects
project_directory = 'C:/Users/vishn/project_rushitha/cloned_projects'


# Function to count the number of functions in the project
def count_functions_in_project(project_path):
    function_count = 0
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):  # Only count functions in Python files
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        for line in f:
                            if re.match(r'^\s*def\s+', line):  # Regex to find function definitions
                                function_count += 1
                except Exception as e:
                    print(f"Error reading file {file}: {e}")
    return function_count

# Function to count operators, operands, and lines of code (this remains the same)
def count_operators_operands(project_path):
    operators = 0
    operands = 0
    lines_of_code = 0

    operator_pattern = re.compile(r'[\+\-\*/=<>]+')  # Basic operators
    operand_pattern = re.compile(r'\b\w+\b')  # Words or variables

    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        for line in f:
                            lines_of_code += 1
                            operators += len(operator_pattern.findall(line))
                            operands += len(operand_pattern.findall(line))
                except Exception as e:
                    print(f"Error reading file {file}: {e}")
                        
    return operators, operands, lines_of_code

# Function to calculate Halstead Volume (round to 2 decimal places)
def calculate_halstead_volume(operators, operands):
    if operators > 0 or operands > 0:
        hv = (operators + operands) * math.log2(operators + operands)
        return round(hv, 2)  # Round Halstead Volume to 2 decimal places
    else:
        return 0

# Function to calculate Maintainability Index (with a minimum threshold)
def calculate_maintainability_index(cc, hv, loc, min_mi=10):
    if loc > 0 and hv > 0:
        mi = 171 - (5.2 * math.log(hv)) - (0.23 * cc) - (16.2 * math.log(loc))
        mi = round(mi,2)
        return max(min_mi, mi)  # Set a minimum MI threshold
    else:
        return None

# Function to run Radon and calculate Cyclomatic Complexity
def run_radon(project_path):
    try:
        # Run Radon for Cyclomatic Complexity
        cc_output = subprocess.run(
            [python_executable, '-m', 'radon', 'cc', '-s', project_path],
            capture_output=True,
            text=True
        )
        cc_data = cc_output.stdout

        # Count functions with cyclomatic complexity
        cyclomatic_complexity = cc_data.count('F')  # 'F' refers to function complexity in Radon's output

        return cyclomatic_complexity
    except Exception as e:
        print(f"Error running Radon for {project_path}: {e}")
        return None


# Main function to analyze a project and calculate the metrics
def analyze_project(project_path, project_name):
    try:
        # Count operators, operands, and LOC
        operators, operands, loc = count_operators_operands(project_path)

        # Calculate Halstead Volume
        hv = calculate_halstead_volume(operators, operands)

        # Count functions
        num_functions = count_functions_in_project(project_path)

        # Calculate Cyclomatic Complexity using Radon
        cc = run_radon(project_path)

        # Calculate Maintainability Index
        mi = calculate_maintainability_index(cc, hv, loc)

        return loc, num_functions, operators, cc, hv, mi
    except Exception as e:
        print(f"Error analyzing project {project_path}: {e}")
        return None, None, None, None, None, None

# List to store all projects
project_data = []

# Loop through project directories and analyze
for project in os.listdir(project_directory):
    project_path = os.path.join(project_directory, project)

    if os.path.isdir(project_path):
        print(f"Analyzing project: {project}")

        # Get all required metrics for the project
        loc, num_functions, operators, cc, hv, mi = analyze_project(project_path, project)

        # Append results
        project_data.append({
            'Project': project,
            'Lines of Code': loc,
            'Number of Functions': num_functions,
            'Number of Operators': operators,
            'Cyclomatic Complexity': cc,
            'Halstead Volume': hv,
            'Maintainability Index': mi
        })

# Convert project data to a DataFrame
df = pd.DataFrame(project_data)

# Save the data to a CSV file
csv_file_path = os.path.join(os.getcwd(), 'project_analysis_with_metrics.csv')
df.to_csv(csv_file_path, index=False)

print(f"Project analysis results saved to {csv_file_path}")
