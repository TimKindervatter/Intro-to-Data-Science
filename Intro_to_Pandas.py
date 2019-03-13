#%%

import pandas as pd


#%% [markdown]
#$\alpha + \frac{\beta}{\gamma} - \delta = 1$


#%%
#Specifying which columns to scrape from the database
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']

#Reading in user data from the database
users = pd.read_csv(
    'http://files.grouplens.org/datasets/movielens/ml-100k/u.user',
    sep='|', names=u_cols)

#Displaying the dataframe
users.head()


#%%
#Specifying which columns to scrape from the database
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']

#Reading in ratings data from the database
ratings = pd.read_csv(
    'http://files.grouplens.org/datasets/movielens/ml-100k/u.data',
    sep='\t', names=r_cols)

ratings.head()


#%%
# the movies file contains columns indicating the movie's genres
# let's only load the first five columns of the file with usecols
m_cols = ['movie_id', 'title', 'release_date', 
            'video_release_date', 'imdb_url']

#Reading in movie data from the database
movies = pd.read_csv(
    'http://files.grouplens.org/datasets/movielens/ml-100k/u.item', 
    sep='|', names=m_cols, usecols=range(5), encoding='latin-1')

movies.head()


#%%
#Logically indexing the users dataframe
#We filter down to only male users aged 40
male_40_users = users[(users.age == 40) & (users.sex == 'M')]

#Filter down to only users who are female programmers
female_programmers = users[(users.sex == 'F') & (users.occupation == 'programmer')]

#Outputs some statistics about the filtered dataframes
male_40_users.describe()
female_programmers.describe()


#%%
#Gets the number of ratings for each movie ID, grouped by 
grouped_data = ratings['movie_id'].groupby(ratings['user_id'])

ratings_per_user = grouped_data.count()

ratings_per_user.head(5)


#%%
#Group all ratings by movie ID
ratings_by_movie = ratings['rating'].groupby(ratings['movie_id'])

#Compute the average rating for each movie ID
average_rating_by_movie = ratings_by_movie.mean()
average_rating_by_movie.head(5)


#%%
#An alternate way to get the average rating for each movie is to use a lambda
average_ratings = ratings_by_movie.apply(lambda f: f.mean())
print(average_ratings.head())

average_rating_by_movie.head()


#%%
#Sort the array in descending order and extract the top 10 values (top 10 highest rated movies)
highest_average_ratings = average_rating_by_movie.sort_values(ascending = False)[0:10]
#Use the indices of these ratings to index the movies.title series
# and obtain the titles of the top rated moves 
# (off by one because movie.title is 0-based indexed)
highest_rated_titles = movies.title[highest_average_ratings.index.values-1]
highest_rated_titles.head(10)


#%%
#Never heard of these movies, might be highly rated because there are few ratings
#Count the number of ratings given to each movie
number_of_ratings = ratings_by_movie.count()
#Index this using the indices of the highest rated movies
#number_of_ratings is 1-based indexed, so no off-by-one
number_of_ratings[highest_average_ratings.index.values]


#%%
ratings_by_user = ratings['rating'].groupby(ratings['user_id'])

average_rating_by_user = ratings_by_user.mean()
average_rating_by_user.head()

#%%
occupation_by_sex = users['sex'].groupby(users['occupation'])

male_dominated_fields = occupation_by_sex.apply(lambda f: sum(f == 'M') > sum(f == 'F'))
print(male_dominated_fields)

print('\nNumber of Male Users:')
print(sum(users['sex'] == 'M'))

print('\nNumber of Female Users:')
print(sum(users['sex'] == 'F'))
#%%
