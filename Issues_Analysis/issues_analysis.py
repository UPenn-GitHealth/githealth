import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import glob

csv_dir = 'Issues_Data/issues_data_v4.0' 

# Pattern to match all CSV files
csv_pattern = os.path.join(csv_dir, 'issues_*.csv')

# Find all CSV files matching the pattern
csv_files = glob.glob(csv_pattern)

print(csv_files)

def generate_issues_first_resp_table(files):
    all_issues_data_list = []
    for file in files:
        df = pd.read_csv(file)
        df['issues_created_at'] = pd.to_datetime(df['issues_created_at'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')
        df = df[~df['issues_created_at'].isnull()]
        df = df.dropna(subset=['issues_time_to_first_response'])
        # Drop duplicate issues based on 'issues_thread_id'
        df = df.drop_duplicates(subset=['issues_thread_id'])
        df['year'] = df['issues_created_at'].dt.year
        df['month'] = df['issues_created_at'].dt.month
        threshold_seconds = 5
        df = df[df['issues_time_to_first_response'] > threshold_seconds]
        if not df.empty:
            all_issues_data_list.append(df)

    if all_issues_data_list:
        all_issues_data = pd.concat(all_issues_data_list, ignore_index=True)
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no data was processed

    sorted_issues_data = all_issues_data.sort_values(by=['year', 'month'])
    # Convert 'issues_time_to_first_response' from seconds to hours for the final table
    sorted_issues_data['issues_time_to_first_response_hours'] = sorted_issues_data['issues_time_to_first_response'] / 3600
    subset_issues_data = sorted_issues_data[['year', 'month', 'issues_time_to_first_response_hours']]
    subset_issues_data.to_csv('issues_first_resp_table.csv', index=False)  # Save to a CSV file
    return subset_issues_data

# Generate and display the sorted issues table
issues_table = generate_issues_first_resp_table(csv_files)
print("Issues table saved to issues_first_resp_table.csv")

def plot_avg_first_resp_time(csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)
    
    # Group by year and month, then calculate the average time to first response
    monthly_avg = data.groupby(['year', 'month'])['issues_time_to_first_response_hours'].mean().reset_index()

    # Convert 'year' and 'month' into a datetime object for plotting
    monthly_avg['date'] = pd.to_datetime(monthly_avg.assign(day=1)[['year', 'month', 'day']])

    # Filter data for the years 2014 to 2023
    start_year = 2014
    end_year = 2023
    monthly_avg = monthly_avg[(monthly_avg['year'] >= start_year) & (monthly_avg['year'] <= end_year)]

    # Save the average time to first response data to a CSV file
    monthly_avg.to_csv('average_response_time_2014_2023.csv', index=False)

    # Plotting the data
    plt.figure(figsize=(15, 7))
    plt.plot(monthly_avg['date'], monthly_avg['issues_time_to_first_response_hours'], marker='o')

    plt.title('Average Time to First Response by Month (2014-2023)')
    plt.xlabel('Date')
    plt.ylabel('Average Time to First Response (Hours)')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.grid(True)

    # Save the plot as an image
    plt.savefig('avg_first_resp_time_plot.png', bbox_inches='tight')

plot_avg_first_resp_time('issues_first_resp_table.csv')

def generate_issues_close_table(files):
    all_issues_data_list = []
    for file in files:
        df = pd.read_csv(file)
        df['issues_created_at'] = pd.to_datetime(df['issues_created_at'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')
        df = df[~df['issues_created_at'].isnull()]
        df = df.dropna(subset=['issues_time_to_close'])
        df = df.drop_duplicates(subset=['issues_thread_id'])
        df['year'] = df['issues_created_at'].dt.year
        df['month'] = df['issues_created_at'].dt.month
        threshold_seconds = 5
        df = df[df['issues_time_to_close'] > threshold_seconds]
        if not df.empty:
            all_issues_data_list.append(df)

    if all_issues_data_list:
        all_issues_data = pd.concat(all_issues_data_list, ignore_index=True)
    else:
        return pd.DataFrame()

    sorted_issues_data = all_issues_data.sort_values(by=['year', 'month'])
    sorted_issues_data['issues_time_to_close_hours'] = sorted_issues_data['issues_time_to_close'] / 3600
    subset_issues_data = sorted_issues_data[['year', 'month', 'issues_time_to_close_hours']]
    subset_issues_data.to_csv('issues_close_table.csv', index=False)
    return subset_issues_data

issues_close_table = generate_issues_close_table(csv_files)
print("Issues close table saved to issues_close_table.csv")

def plot_avg_close_time(csv_file):
    data = pd.read_csv(csv_file)
    monthly_avg = data.groupby(['year', 'month'])['issues_time_to_close_hours'].mean().reset_index()
    monthly_avg['date'] = pd.to_datetime(monthly_avg.assign(day=1)[['year', 'month', 'day']])
    start_year = 2014
    end_year = 2023
    monthly_avg = monthly_avg[(monthly_avg['year'] >= start_year) & (monthly_avg['year'] <= end_year)]
    monthly_avg.to_csv('average_close_time_2014_2023.csv', index=False)
    
    plt.figure(figsize=(15, 7))
    plt.plot(monthly_avg['date'], monthly_avg['issues_time_to_close_hours'], marker='o')
    plt.title('Average Time to Close Issues by Month (2014-2023)')
    plt.xlabel('Date')
    plt.ylabel('Average Time to Close (Hours)')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.grid(True)

    # Save the plot as an image
    plt.savefig('avg_close_time_plot.png', bbox_inches='tight')

plot_avg_close_time('issues_close_table.csv')

def generate_issues_median_first_resp_table(files):
    all_issues_data_list = []
    for file in files:
        df = pd.read_csv(file)
        df['issues_created_at'] = pd.to_datetime(df['issues_created_at'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')
        df = df[~df['issues_created_at'].isnull()]
        df = df.dropna(subset=['issues_time_to_first_response'])
        # Drop duplicate issues based on 'issues_thread_id'
        df = df.drop_duplicates(subset=['issues_thread_id'])
        df['year'] = df['issues_created_at'].dt.year
        df['month'] = df['issues_created_at'].dt.month
        threshold_seconds = 5
        df = df[df['issues_time_to_first_response'] > threshold_seconds]
        if not df.empty:
            all_issues_data_list.append(df)

    if all_issues_data_list:
        all_issues_data = pd.concat(all_issues_data_list, ignore_index=True)
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no data was processed

    sorted_issues_data = all_issues_data.sort_values(by=['year', 'month'])
    # Convert 'issues_time_to_first_response' from seconds to hours for the final table
    sorted_issues_data['issues_time_to_first_response_hours'] = sorted_issues_data['issues_time_to_first_response'] / 3600
    # Calculate the median time to first response for each month
    median_first_resp_times = sorted_issues_data.groupby(['year', 'month'])['issues_time_to_first_response_hours'].median().reset_index()
    median_first_resp_times.to_csv('median_first_response_time_2014_2023.csv', index=False)  # Save to a CSV file
    return median_first_resp_times

# Generate and display the median response times table
median_first_resp_table = generate_issues_median_first_resp_table(csv_files)
print("Median response times table saved to median_first_response_time_2014_2023.csv")

def plot_median_first_resp_time(csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)
    
    # Convert 'year' and 'month' into a datetime object for plotting
    data['date'] = pd.to_datetime(data.assign(day=1)[['year', 'month', 'day']])

    # Filter data for the years 2014 to 2023
    start_year = 2014
    end_year = 2023
    data = data[(data['year'] >= start_year) & (data['year'] <= end_year)]

    # Plotting the data
    plt.figure(figsize=(15, 7))
    plt.plot(data['date'], data['issues_time_to_first_response_hours'], marker='o')

    plt.title('Median Time to First Response by Month (2014-2023)')
    plt.xlabel('Date')
    plt.ylabel('Median Time to First Response (Hours)')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.grid(True)

    # Save the plot as an image
    plt.savefig('median_first_resp_time_plot.png', bbox_inches='tight')

plot_median_first_resp_time('median_first_response_time_2014_2023.csv')

def generate_issues_median_close_table(files):
    all_issues_data_list = []
    for file in files:
        df = pd.read_csv(file)
        df['issues_created_at'] = pd.to_datetime(df['issues_created_at'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')
        df = df[~df['issues_created_at'].isnull()]
        df = df.dropna(subset=['issues_time_to_close'])
        # Drop duplicate issues based on 'issues_thread_id'
        df = df.drop_duplicates(subset=['issues_thread_id'])
        df['year'] = df['issues_created_at'].dt.year
        df['month'] = df['issues_created_at'].dt.month
        threshold_seconds = 5
        df = df[df['issues_time_to_close'] > threshold_seconds]
        if not df.empty:
            all_issues_data_list.append(df)

    if all_issues_data_list:
        all_issues_data = pd.concat(all_issues_data_list, ignore_index=True)
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no data was processed

    sorted_issues_data = all_issues_data.sort_values(by=['year', 'month'])
    # Convert 'issues_time_to_close' from seconds to hours for the final table
    sorted_issues_data['issues_time_to_close_hours'] = sorted_issues_data['issues_time_to_close'] / 3600
    # Calculate the median time to close for each month
    median_close_times = sorted_issues_data.groupby(['year', 'month'])['issues_time_to_close_hours'].median().reset_index()
    median_close_times.to_csv('median_close_time_2014_2023.csv', index=False)  # Save to a CSV file
    return median_close_times

# Generate and display the median close times table
median_close_table = generate_issues_median_close_table(csv_files)
print("Median close times table saved to median_close_time_2014_2023.csv")

def plot_median_close_time(csv_file):
    data = pd.read_csv(csv_file)
    data['date'] = pd.to_datetime(data.assign(day=1)[['year', 'month', 'day']])
    start_year = 2014
    end_year = 2023
    data = data[(data['year'] >= start_year) & (data['year'] <= end_year)]

    # Plotting the data
    plt.figure(figsize=(15, 7))
    plt.plot(data['date'], data['issues_time_to_close_hours'], marker='o')

    plt.title('Median Time to Close Issues by Month (2014-2023)')
    plt.xlabel('Date')
    plt.ylabel('Median Time to Close (Hours)')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.grid(True)

    # Save the plot as an image
    plt.savefig('median_close_time_plot.png', bbox_inches='tight')

plot_median_close_time('median_close_time_2014_2023.csv')
