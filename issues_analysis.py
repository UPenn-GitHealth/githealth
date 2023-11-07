import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# Directory where CSV files are stored
csv_dir = 'Issues_Data/Issues_Data_v3.0/Database'  # Make sure this path is correct

# Pattern to match all CSV files
csv_pattern = os.path.join(csv_dir, 'issues_*.csv')

# Find all CSV files matching the pattern
csv_files = glob.glob(csv_pattern)

# Initialize a DataFrame to hold all data
all_data = pd.DataFrame()

# Define a function to process each CSV and append the data to all_data DataFrame
def process_csv(file_path, all_data):
    df = pd.read_csv(file_path)
    # Convert the 'Created_at' column to datetime
    df['Created_at'] = pd.to_datetime(df['Created_at'])

    # Assume there's a "Time_to_First_Response" column with time in minutes

    # # Debugging to see Time_to_First_Response values for a given csv file
    # df_2023 = df[df['Created_at'].dt.year == 2023]
    # if not df_2023.empty:
    #     print(df_2023[['Created_at', 'Time_to_First_Response']])
 
    # Group the data by month
    df['Month'] = df['Created_at'].dt.to_period('M')
    all_data = pd.concat([all_data, df[['Month', 'Time_to_First_Response']]], ignore_index=True)
    return all_data

for csv_file in csv_files:
    all_data = process_csv(csv_file, all_data)

# Calculate the average Time_to_First_Response for each month
average_response_times_by_month = all_data.groupby('Month')['Time_to_First_Response'].mean().reset_index()

# Plot the data
plt.figure(figsize=(15, 5))
plt.plot(average_response_times_by_month['Month'].astype(str), average_response_times_by_month['Time_to_First_Response'], marker='o')
plt.title('Average Time to First Response By Month')
plt.xlabel('Month')
plt.ylabel('Average Time to First Response (in minutes)')
plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
plt.tight_layout()  # Adjust layout so everything fits without overlapping
plt.grid(True)
plt.show()
