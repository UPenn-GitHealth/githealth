from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List
import os
import glob

app = FastAPI()

# Define a Pydantic model for the response data structure
class IssueResponseTime(BaseModel):
    year: int
    month: int
    issues_time_to_first_response_hours: float

@app.get("/issues/first-response-time", response_model=List[IssueResponseTime])
async def generate_issues_first_resp_table():
    csv_dir = 'Issues_Data/issues_data_v4.0' 
    csv_pattern = os.path.join(csv_dir, 'issues_*.csv')
    csv_files = glob.glob(csv_pattern)

    all_issues_data_list = []

    for file in csv_files:
        df = pd.read_csv(file)
        df['issues_created_at'] = pd.to_datetime(df['issues_created_at'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')
        df = df[~df['issues_created_at'].isnull()]
        df = df.dropna(subset=['issues_time_to_first_response'])
        df = df.drop_duplicates(subset=['issues_thread_id'])
        df['year'] = df['issues_created_at'].dt.year
        df['month'] = df['issues_created_at'].dt.month
        threshold_seconds = 5
        df = df[df['issues_time_to_first_response'] > threshold_seconds]

        if not df.empty:
            all_issues_data_list.append(df)

    if not all_issues_data_list:
        raise HTTPException(status_code=404, detail="No issues data found")

    all_issues_data = pd.concat(all_issues_data_list, ignore_index=True)
    all_issues_data['issues_time_to_first_response_hours'] = all_issues_data['issues_time_to_first_response'] / 3600

    sorted_issues_data = all_issues_data.sort_values(by=['year', 'month'])
    response_data = sorted_issues_data[['year', 'month', 'issues_time_to_first_response_hours']]
    
    # Convert the pandas DataFrame to a list of dictionaries
    response_list = response_data.to_dict(orient='records')
    
    return response_list
