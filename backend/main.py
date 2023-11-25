from typing import Union
# %pip install pandas
# %pip install numpy
# %pip install panel
# %pip install hvplot
# %pip install jupyter_bokeh
import pandas as pd
import numpy as np
import panel as pn
pn.extension('tabulator')
import hvplot.pandas
import calendar

from fastapi import FastAPI

app = FastAPI()

df = pd.read_csv("data_testing.csv")

idf = df.interactive()

pulls_per_repo = (
    idf.groupby(['Repository'])
    .size()
    .reset_index(name='Pull_Request_Count')
    .set_index(['Repository'])
    .sort_values(by=['Pull_Request_Count'], ascending=False)
)
pulls_per_repo

open_pulls_per_repo = (
    # only include open pull requests
    idf[idf['PR_Status'] == 'open']
    .groupby(['Repository'])
    .size()
    .reset_index(name='Open_Pull_Request_Count')
    .set_index(['Repository'])
    .sort_values(by=['Open_Pull_Request_Count'], ascending=False)
)
pulls_per_repo

df['Start_month'] = df['Start_month'].apply(lambda x: '{0:0>2}'.format(x))
df['Start_year_month'] = df['Start_year'].astype(str) + '-' + df['Start_month'].astype(str)

pulls_per_month = (
    idf.groupby(['Start_year_month'])
    .size()
    .reset_index(name='Monthly_Pulls')
    .set_index(['Start_year_month'])
    .sort_values(by=['Start_year_month'], ascending=True)
)
pulls_per_month

# filter out rows with NaN End_time values

df = df[df['End_time'].notna()]

# calculate the time to merge for each pull request in days

df['Days_to_Merge'] = (pd.to_datetime(df['End_time']) - pd.to_datetime(df['Start_time'])).dt.days

# sort rows by End_time

df = df.sort_values(by=['End_time'], ascending=True)

# calculate the rolling average of time to merge for each pull request in days

df['Rolling_Avg_Days_to_Merge'] = df['Days_to_Merge'].rolling(window=100).mean()

# remove the first 99 rows (which have NaN values for the rolling average)

df = df.iloc[99:]

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/items/pulls_per_repo")
def get_pulls():
    return pulls_per_repo.to_dict(orient='records')

@app.get("/items/open_pulls_per_repo")
def get_open_pulls():
    return open_pulls_per_repo.to_dict(orient='records')

@app.get("/items/pulls_per_month")
def get_pulls_per_month():
    return pulls_per_month.to_dict(orient='records')

@app.get("/items/rolling_avg_days_to_merge")
def get_rolling_avg_days_to_merge():
    return df['Rolling_Avg_Days_to_Merge'].to_dict()
