import pandas as pd

# Load the two CSV files
github_projects_with_domain = pd.read_csv('github_projects_with_domains.csv')
github_radon_merged = pd.read_csv('radon_analysis_results.csv')
project_analysis = pd.read_csv('project_analysis_with_metrics.csv')

# Display the first few rows of both dataframes to check their structure
print("GitHub + Radon Merged Data:")
print(github_radon_merged.head())

print("\nProject Analysis Data:")
print(project_analysis.head())

# Select only the necessary columns from the project_analysis_with_metrics
project_analysis_filtered = project_analysis[['Project', 'Lines of Code', 'Number of Functions', 'Number of Operators']]


merged_data = pd.merge(github_projects_with_domain, github_radon_merged, on='Project', how='left')
# Merge the dataframes on the 'Project' column, keeping the new columns
final_merged_data = pd.merge(merged_data, project_analysis_filtered, on='Project', how='left')

# Display the first few rows of the final merged dataframe
print("\nFinal Merged Data:")
print(final_merged_data.head())

# Save the final merged result to a new CSV file
final_merged_data.to_csv('final_merged_github_analysis.csv', index=False)

print("Data merged successfully. Results saved to 'final_merged_github_analysis.csv'.")
