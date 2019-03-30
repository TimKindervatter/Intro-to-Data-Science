#%%
import matplotlib.pyplot as plt
import pandas as pd

#%%
#Read global list of countries and global income data from online data sets
world_atlas = pd.read_csv('https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv')
global_income = pd.read_excel('https://docs.google.com/spreadsheet/pub?key=phAwcNAVuyj1jiMAkmq1iMg&output=xlsx')
global_income = global_income.rename(index=str, columns={'GDP per capita': 'Country'})

#%%
#By default, data is organized into columns by year
#It may be useful to organize columns by country instead, which we can do by transposing the dataframe
transposed_income = global_income.transpose()
transposed_income.head()

#%%
year = 2000
plt.hist(global_income[2000], bins=50)
plt.title('Global Income Distribution in {}'.format(year))
plt.xlabel('GDP Per Capita')
plt.ylabel('Number of Countries')

#%%
def merge_by_year(year):
    """
    Returns a merged data frame containing the income, 
    country name and region for a given year. 

    Args:
        year (int): The year of interest

    Returns:
        income_by_region (data frame): A pandas DataFrame with three columns titled 'Country', 'Region', and 'GDP Per Capita'. 
    """

    income = pd.DataFrame(global_income[['Country', year]])
    income = income.rename(index=int, columns={year: 'GDP Per Capita'})
    joined = pd.merge(world_atlas, income, how='inner', on='Country')
    return joined

#%%
regions = world_atlas['Region'].unique()
income_by_region = {region: None for region in regions}
for year in range(1900,2010,10):
    data_this_year = merge_by_year(year)
    for region in regions:
        filtered_by_region = data_this_year[data_this_year['Region'] == region]
        income_by_region[region] = filtered_by_region['GDP Per Capita'].values

        plt.hist(income_by_region[region])
        plt.ylim(0,30)
        plt.title('GDP Per Capita in {}'.format(region.title()))
        plt.xlabel('GDP Per Capita')
        plt.ylabel('Number of Countries')
        plt.show()

    data_this_year.boxplot('GDP Per Capita', by='Region', rot=45)
    plt.title('GDP Per Capita in {}'.format(year))
    plt.ylabel('GDP Per Capita (log scale)')
    plt.yscale('log')
    plt.show()

#%%
