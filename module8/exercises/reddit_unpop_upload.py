## Include whichever API are appropriate for your cloud provider

#----------------------------Reddit RSS Feed----------------------------------------
# For my project, I will run the RSS feed on the subreddit 
# r/unpopularopinion/
#-----------------------------------------------------------------------------------

import os
from google.cloud import storage
## Change to your own project name
PROJECT='lcmhng-mu-dsa'

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)

def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    """Lists all the blobs in the bucket that begin with the prefix.
    This can be used to list all blobs in a "folder", e.g. "public/".
    The delimiter argument can be used to restrict the results to only the
    "files" in the given "folder". Without the delimiter, the entire tree under
    the prefix is returned. For example, given these blobs:
        /a/1.txt
        /a/b/2.txt
    If you just specify prefix = '/a', you'll get back:
        /a/1.txt
        /a/b/2.txt
    However, if you specify prefix='/a' and delimiter='/', you'll get back:
        /a/1.txt
    """
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)

    print('Blobs:')
    for blob in blobs:
        print(blob.name)

    if delimiter:
        print('Prefixes:')
        for prefix in blobs.prefixes:
            print(prefix)

#------------------------------------------------------------------------UPLOAD----------------------------

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def upload_as_blob(bucket_name, source_data, destination_blob_name, content_type='text/plain'):
    """Uploads a file to the bucket."""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    #blob.upload_from_filename(source_file_name)
    blob.upload_from_string(source_data, content_type=content_type)
    
    print('Data uploaded to {}.'.format(destination_blob_name))

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print('Blob {} deleted.'.format(blob_name))

#-------------------------RUNTIME CODE

# Bucket Name:
#my_bucket_name = 'dsa_mini_project_lcmhng'
my_bucket_name = 'dsa_project_lcmhng'

list_blobs(my_bucket_name)

#------------------------------Update with REDDIT download

def read_blob(bucket_name, source_blob_name):
    """Downloads a blob from the bucket and returns content in bytearray"""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    return blobdownload_as_string()

def read_blob_as_string(bucket_name, source_blob_name):
    """Downloads a blob from the bucket and returns content in string"""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    return blob.download_as_string().decode("utf-8") 

#-----------------------------------CODE TO GRAB AND STORE REDDIT DATA

import feedparser
from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd
import numpy as np

# Functions from: https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

# Define URL of the RSS Feed I want
# Here we will update to the specific subreddit of choice r/unpopularopinion/

a_reddit_rss_url = 'http://www.reddit.com/r/unpopularopinion/.rss?sort=new'

feed = feedparser.parse( a_reddit_rss_url )

"""
if (feed['bozo'] == 1):
    print("Error Reading/Parsing Feed XML Data")    
else:
    for item in feed[ "items" ]:
        dttm = item[ "date" ]
        title = item[ "title" ]
        summary_text = text_from_html(item[ "summary" ])
        link = item[ "link" ]
        
        print("====================")
        print("Title: {} ({})\nTimestamp: {}".format(title,link,dttm))
        print("--------------------\nSummary:\n{}".format(summary_text))
   
"""
              
# ------------ Create file string
"""         
def reddit_post_string(feed):
"""
    #Funciton to generate text for JSON file from reddit rss
"""    
    
    file_str = ""
              
    if (feed['bozo'] == 1):
        print("Error Reading/Parsing Feed XML Data")    
    else:
        for item in feed[ "items" ]:
            dttm = item[ "date" ]
            title = item[ "title" ]
            summary_text = text_from_html(item[ "summary" ])
            link = item[ "link" ]
        
            file_str += "====================\n"
            file_str += "Title: {} ({})\nTimestamp: {}\n".format(title,link,dttm)
            file_str += "--------------------\nSummary:\n{}".format(summary_text)

    return file_str
"""
#---------------------------------------Creating a file name------------------

import time
timestr = time.strftime("%Y%m%d-%H%M%S")
print(timestr)

file_name = "reddit-unpop-rss-" + timestr + ".txt"
## print(file_name)
#reddit_thread_string = reddit_post_string(feed)

# I actually should not need this code---------------------------------------------------------------
# unpop_df = pd.DataFrame.from_dict(feed["items"])
# Instead we should just be able to upload the scraped feed as is which would save as JSON

#upload_as_blob(my_bucket_name, reddit_thread_string, file_name)
# THIS IS ANOTHER OLDER VERSION SAVING THE DATAFRAME -------------> upload_as_blob(my_bucket_name, unpop_df, file_name)
upload_as_blob(my_bucket_name, feed, file_name)

# list_blobs(my_bucket_name)