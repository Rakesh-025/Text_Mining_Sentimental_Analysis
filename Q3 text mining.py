import requests   # Importing requests to extract content from a url
from bs4 import BeautifulSoup as bs # Beautifulsoup is for web scrapping...used to scrap specific content 
import re

from wordcloud import WordCloud
import matplotlib.pyplot as plt


# creating empty reviews list
kingbed_reviews=[]

for i in range(1,4):
  ip=[]  
  url="https://www.flipkart.com/hometown-engineered-wood-king-box-bed/product-reviews/itme370aed3f4e20?pid=BDDF8K2SGHXSJEFR&lid=LSTBDDF8K2SGHXSJEFRHS93AN&marketplace=FLIPKART"+str(i)  
  response = requests.get(url)
  soup = bs(response.content,"html.parser")# creating soup object to iterate over the extracted content 
  reviews = soup.find_all("div", attrs={"class","K0kLPL"})# Extracting the content under specific tags  
  for i in range(len(reviews)):
    ip.append(reviews[i].text)  
 
  kingbed_reviews = kingbed_reviews + ip  # adding the reviews of one page to empty list which in future contains all the reviews

# writng reviews in a text file 
# saving the reviews in a textt file i.e., oneplus as text file
with open("kingbed_reviews.txt", "w", encoding='utf8') as output:
    output.write(str(kingbed_reviews))


import os
os.getcwd()

	

# Joinining all the reviews into single paragraph 
ip_rev_string = " ".join(kingbed_reviews)

import nltk
# from nltk.corpus import stopwords

# Removing unwanted symbols incase if exists
ip_rev_string = re.sub("[^A-Za-z" "]+", " ", ip_rev_string).lower()
# ip_rev_string = re.sub("[0-9" "]+"," ", ip_rev_string)

# words that contained in the reviews
ip_reviews_words = ip_rev_string.split(" ")

ip_reviews_words = ip_reviews_words[1:]

#TFIDF
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(ip_reviews_words, use_idf=True, ngram_range=(1, 1))
X = vectorizer.fit_transform(ip_reviews_words)

with open("C:/Users/kaval/OneDrive/Desktop/360digit/datatypes/stop.txt", "r") as sw:
    stop_words = sw.read()
    
stop_words = stop_words.split("\n")

ip_reviews_words = [w for w in ip_reviews_words if not w in stop_words]

# Joinining all the reviews into single paragraph 
ip_rev_string = " ".join(ip_reviews_words)

# WordCloud can be performed on the string inputs.
# Corpus level word cloud

wordcloud_ip = WordCloud(background_color='White',
                      width=1800,
                      height=1400
                     ).generate(ip_rev_string)
plt.imshow(wordcloud_ip)

# positive words # Choose the path for +ve words stored in system
with open("C:/Users/kaval/OneDrive/Desktop/360digit/datatypes/positive-words.txt","r") as pos:
  poswords = pos.read().split("\n")

# Positive word cloud
# Choosing the only words which are present in positive words
ip_pos_in_pos = " ".join ([w for w in ip_reviews_words if w in poswords])

wordcloud_pos_in_pos = WordCloud(
                      background_color='White',
                      width=1800,
                      height=1400
                     ).generate(ip_pos_in_pos)
plt.figure(2)
plt.imshow(wordcloud_pos_in_pos)

# negative words Choose path for -ve words stored in system
with open("C:/Users/kaval/OneDrive/Desktop/360digit/datatypes/negative-words.txt", "r") as neg:
  negwords = neg.read().split("\n")

# negative word cloud
# Choosing the only words which are present in negwords
ip_neg_in_neg = " ".join ([w for w in ip_reviews_words if w in negwords])

wordcloud_neg_in_neg = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(ip_neg_in_neg)
plt.figure(3)
plt.imshow(wordcloud_neg_in_neg)

