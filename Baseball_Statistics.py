#%%
import requests
import zipfile
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt

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
for year in range(2000,2004,1):
    #Filter the data frame down to only the current year's data
    data_by_year = merged_df[(merged_df.yearID == year)]
    
    #Create a scatter plot for the current year's data
    plt.scatter(data_by_year['salary'], data_by_year['W'])
    plt.title('Salary vs. Wins for All Teams in {}'.format(year))
    plt.xlabel('Salary (USD)')
    plt.ylabel('Number of Wins')

    #Label the Oakland data point in each figure
    data_by_year['teamID'].str.contains('OAK')
    OAK_data_point = (data_by_year['salary'][data_by_year['teamID'] == 'OAK'], 
    data_by_year['W'][data_by_year['teamID'] == 'OAK'])
    plt.annotate('OAK', OAK_data_point, xytext=(5,0), textcoords='offset points')
    
    plt.show()

#%%
