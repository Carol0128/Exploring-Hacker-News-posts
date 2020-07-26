#!/usr/bin/env python
# coding: utf-8

# # Project
# **Exploring Hacker News Posts**
# 
# Hacker News is a site started by the startup incubator [Y Combinator](https://www.ycombinator.com/), where user-submitted stories (known as "posts") are voted and commented upon, similar to reddit. Hacker News is extremely popular in technology and startup circles, and posts that make it to the top of Hacker News' listings can get hundreds of thousands of visitors as a result.
# 
# The data set can be found [here](https://www.kaggle.com/hacker-news/hacker-news-posts), but it has been reduced from almost 300,000 rows to approximately 20,000 rows by removing all submissions that did not receive any comments, and then randomly sampling from the remaining submissions. Below are descriptions of the columns:
# 
# - id: The unique identifier from Hacker News for the post
# - title: The title of the post
# - url: The URL that the posts links to, if it the post has a URL
# - num_points: The number of points the post acquired, calculated as the total number of upvotes minus the total number of downvotes
# - num_comments: The number of comments that were made on the post
# - author: The username of the person who submitted the post
# - xcreated_at: The date and time at which the post was submitted
# This project's objective is therefore to analyze the posts in the Hacker News site.
# 

# In[1]:


#Reading the hacker_news.csv file:
opened_file = open('hacker_news.csv')
from csv import reader
read_file = reader(opened_file)
hn = list(read_file)
hn[:5]


# In[2]:


#extracting the header
headers = hn[0]
hn = hn[1:]
print(headers)
hn[:5]


# Having removed the headers from hn, we're ready to filter our data. Since we're only concerned with post titles beginning with Ask HN or Show HN, we'll create new lists of lists containing just the data for those titles.
# We'll use the string ,method *startswith*

# In[3]:


#create empty lists
ask_posts = []
show_posts = []
other_posts = []

#looping through each row to find number of posts in each of
#the stated categories

for row in hn:
    title = row[1]
    
    if title.lower().startswith('ask hn'):
        ask_posts.append(row)
    elif title.lower().startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(title)
        
print('The number of ask posts is: ' + str(len(ask_posts)))
print('The number of show posts is: ' + str(len(show_posts)))
print('The number of other posts is: ' + str(len(other_posts)))

        


# The code above has separated the "ask posts" and the "show posts" into two list of lists named ask_posts and show_posts.
# 
# Next, we'll determine which, among the two, received more comments on average.

# In[4]:


print(ask_posts[:3])


# In[5]:


total_ask_comments = 0
for item in ask_posts:
    num_comments = int(item[4])
    total_ask_comments += num_comments
avg_ask_comments = total_ask_comments/len(ask_posts)
print('The average comments on ask posts is: ' + str(avg_ask_comments))

total_show_comments = 0
for item in show_posts:
    num_comments = int(item[4])
    total_show_comments += num_comments
avg_show_comments = total_show_comments/len(show_posts)
print('The average comments on show posts is: ' + str(avg_show_comments)
     )


# From the output above, ask posts receive more comments on average.
# 
# Next, we'll determine if ask posts created at a certain time are more likely to attract comments. We'll use the following steps to perform this analysis:
# 
# 1. Calculate the amount of ask posts created in each hour of the day, along with the number of comments received.
# 2. Calculate the average number of comments ask posts receive by hour created.

# In[6]:


import datetime as dt
result_list = []
for post in ask_posts:
    date_created = post[6]
    num_of_comments = int(post[4])
    result_list.append([date_created, num_of_comments])
    
counts_by_hour = {}
comments_by_hour = {}

date_format = "%m/%d/%Y %H:%M"

for row in result_list:
    created_date = row[0]
    comment = row[1]
    
    parsed_date = dt.datetime.strptime(created_date, date_format)
    hour_created = parsed_date.strftime("%H")
    
    if hour_created not in counts_by_hour:
        counts_by_hour[hour_created] = 1
        comments_by_hour[hour_created] = comment
    else:
        counts_by_hour[hour_created] += 1
        comments_by_hour[hour_created] += comment 
        
print(comments_by_hour)
print(counts_by_hour)


# We'll use these two dictionaries, _counts_by_hour and comments_by_hour to calculate the average number of comments for posts created during each hour of the day.
# 
# To achieve this, we need to create a list of lists containing the hours during which posts were created and the average number of comments those posts received.
# 

# In[7]:


avg_by_hour = []
for hour_created in comments_by_hour:
    average = (comments_by_hour[hour_created])/ (counts_by_hour[hour_created])
    avg_by_hour.append([hour_created, average ])
    
print("The average number of comments per ask post per hour is: " +
      str(avg_by_hour))
    


# To finish, we need to sort the list of lists to identify hours with highest values, and print the five highest values in a format that's easier to read.

# In[8]:


swap_avg_by_hour = []
for hour in avg_by_hour:
    swap_avg_by_hour.append([hour[1], hour[0]])
    
print(swap_avg_by_hour)


# In[14]:


sorted_swap = sorted(swap_avg_by_hour, reverse = True)
print("Top 5 Hours for Ask Posts Comments")

for row in sorted_swap[:5]:
    average = row[0]
    hour = row[1]
    
    hour_format = "%H"
    new_hour = dt.datetime.strptime(hour, hour_format)
    hour = new_hour.strftime("%H:%M")
    
    output = "{a}: {b:.2f} average comments per post.".format(a = hour, b = average)
    print(output)   
    
        


# **1500hrs(EST)** have the highest average comments per post, therefore it is advisable to create a post at this time to have a higher chance of receiving comments.
