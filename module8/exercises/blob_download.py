import feedparser
from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd
import numpy as np

import os
from google.cloud import storage
## Change to your own project name
PROJECT='lcmhng-mu-dsa'

my_bucket_name = 'dsa_project_lcmhng'

blob_list = []

for blob_item in list_blobs(my_bucket_name):
    blob_list.append(read_blob_as_string(my_bucket_name, blob_item))

new_sum_list = []
    
for blob in blob_list:
    for item in blob["items"]:
        new_sum_list.append(text_from_html(item["summary"]))
    
    
#---------------Saving below for reference-------------
"""   
sum_list = []

for item in feed["items"]:
    sum_list.append(text_from_html(item["summary"]))
"""