#!/usr/bin/env python
# coding: utf-8

# # Free apps and their marketability
# 
# In this project, I am going to analyze types of mobile apps and how many users they attract. Therefore, we are going to compare different free apps with their visibility and popularity. We are going to compare the apps on both Android and iOS platforms. 

# In[1]:


from csv import reader

apple = open('AppleStore.csv')
read_a = reader(apple)
ios = list(read_a)
google = open('googleplaystore.csv')
read_g = reader(google)
android = list(read_g)


# Due to unavailability of the entire data set, we will use the available samples for our analysis (source: *Kaggle*). 

# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))
        
explore_data(android,10471,10474,rows_and_columns=False)
del android[10472]


# In[3]:


#Clean google data set
#Check for duplicates
#Delete duplicate redundant entries

duplicate = []
unique = []

for app in android:
    name = app[0]
   # print(name)
    if name in unique:
        duplicate.append(name)
    else:
        unique.append(name)
        
for app in android:
    name = app[0]
    if name == 'Box':
        print(app)
        
print('Number of duplicate apps = ', len(duplicate))
print('\n')
print('Egs. of duplicate apps', duplicate[:15])
#print(unique)
print('\n')
print('Number of rows in android = ', len(android))
print('\n')
print("No. of unique apps = ", len(android[1:]) - len(duplicate))


# In the previous section we figured that there are duplicate entries for some apps. We also deleted any entry that was missing or was wrong.
# 
# Now we need to remove the redundant entries to stop us from double counting them. In order to do that, we will first create `dictionaries` to map app-names to their number of reviews. We will keep the app-names only when their value in the dictionary is the highest, i.e. we will count the app entries for the highest number of reviews as they are the latest data available. In the next few steps, we will perform this task.

# In[4]:


#Create dictionary {app-name: no. of reviews}
reviews_max = {}

#Once we have this dictionary, 
#we will create a data set with only unique rows

android_clean = []
already_added = []

for app in android[1:]:
    name = app[0]
    n_reviews = (app[3]) #Check if there is 3.0M somewhere in reviews, delete that row
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    if name not in reviews_max:
        reviews_max[name] = n_reviews
        
#print(reviews_max)  
len(reviews_max)

for app in android[1:]:
    name = app[0]
    n_reviews = app[3]
    if (n_reviews == reviews_max[name]) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)
        
print(len(android_clean))        


# Now we have removed any duplicate entries in our Google Play app data set.
# 
# The next step is to remove any apps that do not have **English** names. This is because we are catering to our English-speaking audiences. 
# 
# Using `ordinality` of the English alphabets, given by the **ASCII** codes, we will only keep alphabets that conform to this ordinality, i.e. in the range of `0 to 127`. 
# 
# Before we delete these rows in our data set, we first need to index and find out the app names with these characters which will be our next step.

# In[5]:


def string_log(string):
    for character in string:
        if ord(character) <= 127:
            return True
        else:
            return False
    
string = '😜a'
print(string_log(string))
    
#This method will remove some relevant apps too 
#Therefore, keep atleast 3 non-eng characters

def string_keep(string):
    non_eng = 0
    for character in string:
        if ord(character) > 127:
            non_eng += 1
    if non_eng > 3:
        return False
    else:
        return True

string = '😜乐电a'
print(string_keep(string))

ios_eng = []
android_eng = []

for app in ios[1:]:
    name = app[1]
    keep_name = string_keep(name)
    if (keep_name == True):
        ios_eng.append(app)
       
        
for app in android_clean:
    name = app[0]
    keep_name = string_keep(name)
    if keep_name == True:
        android_eng.append(app)
        
explore_data(android_eng, 0, 10, True)
print('\n')
explore_data(ios_eng, 0, 3, True)        


# ## Isolating the free apps

# In[8]:


ios_free = []
android_free = []

for app in ios_eng:
    price = app[4]
    if price == '0.0':
        ios_free.append(app)
        
for app in android_eng:
    price = app[6]
    if price == 'Free':
        android_free.append(app)
        
print(len(ios_free))
print(len(android_free))


# ## Validation Strategy for an App
# 
# Steps:
# 1. Build a minimal Android version and launch on Google Play
# 2. Develop further if it gets a good response
# 3. If the app is profitable after 6 months, build an iOS version and launch it on Apple Store
# 
# We need to assess profitable apps for both versions.

# In[14]:


print(ios_free[0])
print('\n')
print(android_free[0])


# By inspection of the data set, we need to build a frequency table for the `prime_genre` column in the Apple data set, and for the `Genres` and `Category` column in the Google data set.

# In[20]:


def freq_table(dataset, index):
    table = {}
    freq_genre = 0
    
    for app in dataset:
        genre = app[index]
        freq_genre += 1
        if genre in table:
            table[genre] += 1
        else:
            table[genre] = 1 #This gives us the freq
            
        #Now need to convert freq to percentage 
    table_pp = {}
    for genre in table:
        table_pp[genre] = (table[genre] / freq_genre) * 100
        
    return table_pp

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
        
display_table(ios_free,-5)
print('\n')
display_table(android_free,1)


# ## Analyzing the frequency tables of different genres in iOS and Android apps
# 
# From the above analysis, we learn that in the Apple store data set, amongst the free English-named apps, **Games**, and **Entertainment** are the most common. Games dominate the iOS market by a huge margin. However, there is no such strong domination in the Android market. The Android market has **Family** and **Game** as the most common apps in our observable sub-sample. 
# 
# Based on this analysis, we can recommend Gaming apps (or Entertainment apps) based on the number of apps available alone. However, we need to check user rating and popularity or downloads before making any suggestions. 
# 
# ## Analyzing App popularity
# 
# Now we move on to checking app popularity by checking the number of installs *or* the user ratings.
# 
# In order to do this, we will perform the following steps to first calculate the average user rating in each genre of app in the iOS store:
# 1. Isolate the apps in each genre
# 2. Calculate the average user rating 

# In[38]:


ios_genre_table = freq_table(ios_free,-5)
print(ios_genre_table)
print('\n')

for genre in ios_genre_table:
    total = 0
    len_genre = 0
    for app in ios_free:
        genre_app = app[-5]
        if genre_app == genre:
            rating = float(app[5])
            total += rating
            len_genre += 1
    avg_rating = total/len_genre 
    print(genre)
    print(avg_rating)
    


# From the above table, it seems like `Navigation` dominates the user ratings followed by `Reference` and `Social Networking`. By examination of the data set, Navigation is primarily dominated by Google maps. Therefore, we would suggest coming up with a free app in either of the two latter categories. 
# 
# The same could be true of any category (needs further analysis).

# In[43]:


android_freqtab = freq_table(android_free,1)
print(android_freqtab)
print('\n')

for genre in android_freqtab:
    total = 0
    len_install = 0
    for app in android_free:
        genre_app = app[1]
        if genre_app == genre:
            installs = app[5]
            installs = installs.replace('+','')
            installs = installs.replace(',','')
            installs = float(installs)
            total += installs
            len_install += 1
    abg_installs = total/len_install 
    print(genre)
    print(abg_installs)
    


# 
