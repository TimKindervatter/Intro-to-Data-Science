#%%
import requests
import zipfile
from io import BytesIO
import pandas as pd

#%%
response = requests.get('http://seanlahman.com/files/database/lahman-csv_2014-02-14.zip').content
zipped_folder = zipfile.ZipFile(BytesIO(response))
zipped_folder.namelist()

#%%
salaries = pd.read_csv(zipped_folder.open('Salaries.csv'))
teams = pd.read_csv(zipped_folder.open('Teams.csv'))

#%%
salaries.head()

#%%
teams.head()

#%%
salaries_by_team_by_year = salaries.groupby(['teamID','yearID'], as_index=False).sum()
salaries_by_team_by_year.head()

#%%
merged_df = pd.merge(salaries_by_team_by_year, teams, how='inner', on=['teamID','yearID'])

#%%
merged_df[(merged_df.yearID > 2000) & (merged_df.yearID < 2004)].plot.scatter(x='salary', y='W')

#%%
