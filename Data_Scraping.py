#%%
import urllib.request as urllib
import bs4
import socket
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import re

#Read the html source of the following url
url = 'http://emlab.utep.edu/ee3321emf.htm'
source = urllib.urlopen(url).read().decode('utf8')

#%%
#Returns true or false depending on whether the word is found in the html source
print('Wave' in source)
print('Einstein' in source)

#Prints the number of times Maxwell appears in the html source
print(source.count('Maxwell'))

#Prints the index of the first instance of Faraday in the html source
position = source.find('Faraday')

#Starts at the index found above and prints 20 characters
print(source[position:position + 20])
#Starts at the index found above and prints the number of characters
#in the word Faraday (i.e. it just prints Faraday)
print(source[position:position + len('Faraday')])
 
 #%%


#%%
#Parses the html source using the beautiful soup library
soup = bs4.BeautifulSoup(source)
#Finds all <a> tags in the html source
soup.findAll('a')

#%%
#Finds the first <a> tag in the source
first_tag = soup.find('a')
#Gets the href attribute (the url that a hyperlink points to) from first_tag
first_tag.get('href')

#Gets all urls from the html source
link_list = [l.get('href') for l in soup.findAll('a')]
link_list

#%%
#Filters all the links down to only those linking outside the site
external_links = []

#External links start with http
#Some entries may be NoneType, so we must ignore those
for l in link_list:
    if l is not None and l[:4] == 'http':
        external_links.append(l)

#The above code can also be achieved using a list comprehension
external_links_comprehension = [l for l in link_list if l is not None and l.startswith('http')]

#Showing that the two approaches give the same answer
print(external_links)
print('\n')
print(external_links_comprehension)

#%%
# We can also use beautiful soup to parse local html files
s = """<!DOCTYPE html><html><head><title>This is a title</title></head><body><h3> Test </h3><p>Hello world!</p></body></html>"""
tree = bs4.BeautifulSoup(s)

## get html root node
root_node = tree.html

## get head from root using contents
head = root_node.contents[0]

## get body from root
body = root_node.contents[1]

## could directly access body
tree.body

tree.body.find('h3')

#%%
#We will parse the beautiful soup webpage for its "hall of fame"
url = 'http://www.crummy.com/software/BeautifulSoup'
beautiful_soup_html = urllib.urlopen(url).read()

#The hall of fame is the only unordered list on the page
beautiful_soup_parsed = bs4.BeautifulSoup(beautiful_soup_html)
unordered_list = beautiful_soup_parsed.find('ul')

#Extracting the contents of the unordered html list into a python list
hall_of_fame_list = [li.contents for li in unordered_list.contents[1:]]

#The join function iterates over a list, concatenating each element one by one
#This turns our hall of fame list into one big string
hall_of_fame_string_list = ["".join(str(a) for a in sublist) for sublist in hall_of_fame_list]
print("\n".join(hall_of_fame_string_list))

#%%
#We want to scrape skills listed in job openings for data scientists
#Let's query data science on indeed.com and parse the results
url = 'http://www.indeed.com/jobs?q=data+scientist&start='
source = urllib.urlopen(url).read()
bs_tree = bs4.BeautifulSoup(source)

#Print out the number of data science jobs found by using the searchCount tag
jobs_found = bs_tree.find(id = 'searchCount').contents[0]
jobs_found = jobs_found.split()[-2]
print("{0} data science jobs were found".format(jobs_found))

#jobs_found is still a string, and it has a comma in it, so we can't just cast it to an int
#Here's a solution:
jobs_found_digits = [int(d) for d in jobs_found if d.isdigit()]
jobs_found = sum([d*(10**exp) for d,exp in zip(jobs_found_digits[::-1], range(len(jobs_found_digits)))])

print(jobs_found)

#%%
int_pages = int(np.ceil(jobs_found/10.0))
base_url = 'https://www.indeed.com'
job_links = []

#Loops through several pages of job listings and reads the html of each
for i in range(20):
    if i % 10 == 0:
        print(int_pages - i)
    url = base_url + '/jobs?q=data+scientist&start=' + str(i*10)
    html_page = urllib.urlopen(url).read()
    bs_tree = bs4.BeautifulSoup(html_page)

    #Narrows down html to that of the job listings
    job_link_area = bs_tree.find(id = 'resultsCol')
    job_postings = job_link_area.findAll('div')
    #Adds each job listing to a python list
    job_postings = [jp for jp in job_postings if not jp.get('class') is None 
                    and ''.join(jp.get('class')).startswith("jobsearch-SerpJobCard")]
    #Adds the job id of each job listing to a python list
    job_ids = [jp.get('data-jk') for jp in job_postings]
    
    #Creates a list of urls to scrape based on the job ids
    for id in job_ids:
        job_links.append(base_url + '/rc/clk?jk=' + id)

    #It's best practice to space out requests so the target servers aren't overloaded
    time.sleep(1)

print("{0} jobs were found".format(len(job_links)))

#%%
#We will be scraping the job listings for the following skills
skill_set = {'Python': 0, 'R': 0, 'MATLAB': 0, 'Julia': 0, 'Javascript': 0,
            'Java': 0, 'C': 0, 'Ruby': 0, 'Perl': 0, 'PHP': 0,
            'Scala': 0, 'Rust': 0, 'Go': 0, 'Haskell': 0,
            'SQL': 0, 'noSQL': 0, 'MongoDB': 0,
            'Excel': 0, 'Tableau': 0, 'SAS':0, 'SPSS': 0,
            'numpy': 0, 'pandas': 0,  'scikit': 0, 
            'matplotlib': 0, 'd3': 0, 'ggplot': 0,
            'MapReduce': 0, 'Spark': 0, 'Hadoop': 0}

counter = 0

#Loop through each job listing
for link in job_links:
    counter += 1
    
    #Error handling
    try:
        html_page = urllib.urlopen(link).read().decode('utf8')
    except urllib.HTTPError:
        print("HTTPError:")
        continue
    except urllib.URLError:
        print("URLError:")
        continue
    except socket.error as error:
        print("Connection closed")
        continue

    #Removes (technically, replaces with whitespace) all characters that
    #are not a letter or the number 3
    html_text = re.sub("[^a-z.+3]", " ", html_page.lower())

    #If one of the skills of interest is included in the job listing,
    #increment its value in the dictionary
    for key in skill_set.keys():
        if key.lower() in html_text:
            skill_set[key] += 1

    #Every 5 iterations, print the status to the console
    if counter % 5 == 0:
        print(len(job_links) - counter)
        print(skill_set)

#%%
#Convert the dictionary of skills to a pandas series and sort it
pseries = pd.Series(skill_set)
pseries = pseries.sort_values(ascending=False)

#Create a bar plot of the scraped data
pseries.plot(kind = 'bar', color = 'b')
plt.title('Data Science Skills Mentioned in Job Listings')
plt.xlabel('Skill')
plt.ylabel('Number of Mentions')
plt.show()

#%%
