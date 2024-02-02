import pandas as pd

# Define the file path (change this to the path of your CSV file)
file_path = 'github_discussion_data.csv'

# Read the CSV file using pandas
try:
    df = pd.read_csv(file_path)

    # Display the first few rows of the DataFrame
    print(df.head())
except Exception as e:
    print(f"Error reading the CSV file: {e}")
