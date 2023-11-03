import calendar
import hvplot.pandas
import pandas as pd
import numpy as np
import panel as pn
pn.extension('tabulator')

df = pd.read_csv("data_testing.csv")
print(df.head())
print(df.info())

idf = df.interactive()
year_slider_min = pn.widgets.IntSlider(
    name='Year slider min', start=2018, end=2024, step=1, value=2018)
year_slider_max = pn.widgets.IntSlider(
    name='Year slider max', start=2018, end=2024, step=1, value=2023)

df['Start_year'] = pd.to_datetime(df.Start_time).dt.year
df['Start_month'] = pd.to_datetime(df.Start_time).dt.month
df['Start_day'] = pd.to_datetime(df.Start_time).dt.day
df['End_year'] = pd.to_datetime(df.End_time).dt.year
df['End_month'] = pd.to_datetime(df.End_time).dt.month
df['End_day'] = pd.to_datetime(df.End_time).dt.day

pulls_per_repo = (
    idf.groupby(['Repository'])
    .size()
    .reset_index(name='Pull_Request_Count')
    .set_index(['Repository'])
    .sort_values(by=['Pull_Request_Count'], ascending=False)
)

# show the table
pn.widgets.Tabulator(pulls_per_repo)
