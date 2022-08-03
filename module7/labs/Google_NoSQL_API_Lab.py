#!/usr/bin/env python
# coding: utf-8

# # Google NoSQL Lab

# ## Step 1: Setup and Test
# https://cloud.google.com/datastore/docs/quickstart
#   * **STOP** before the Clean Up step.
# 

# ## Step 2.a:  Create a preemptible instance and install the required packages
# 
# 1.Create a preemptible instance: 
# 
#  https://cloud.google.com/compute/docs/instances/create-start-preemptible-instance 
# 
# 2.Install the following packages
# * sudo apt install python-pip
# * pip install --upgrade google-api-python-client
# * pip install --upgrade google-cloud-datastore

# ## Step 2.b: Run the following command
# 
# * `gcloud auth application-default login`
# 

# ## Step 3: Use Google Cloud SDK Python API
#  * https://cloud.google.com/datastore/docs/datastore-api-tutorial
#    * The below cells are using the Python version!
#    * First read the following cells then go to the bottom of the notebook and follow the instruction there.

# In[ ]:


import json

import googleapiclient.discovery


# In[ ]:


from google.cloud import datastore


def create_client(project_id):
    return datastore.Client(project_id)


# In[ ]:


def add_task(client, description):
    key = client.key('Task')

    task = datastore.Entity(
        key, exclude_from_indexes=['description'])

    task.update({
        'created': datetime.datetime.utcnow(),
        'description': description,
        'done': False
    })

    client.put(task)

    return task.key


# In[ ]:


def mark_done(client, task_id):
    with client.transaction():
        key = client.key('Task', task_id)
        task = client.get(key)

        if not task:
            raise ValueError(
                'Task {} does not exist.'.format(task_id))

        task['done'] = True

        client.put(task)


# In[ ]:


def delete_task(client, task_id):
    key = client.key('Task', task_id)
    client.delete(key)


# In[ ]:


def list_tasks(client):
    query = client.query(kind='Task')
    query.order = ['created']

    return list(query.fetch())


# In[ ]:


import requests
requests.get('https://google.com/')


# In[ ]:


project_id = 'cloudclassm7' # Replace it with your project ID
gcp_client = create_client(project_id)
results = list_tasks(gcp_client)


# In[ ]:


for r in results:
    print(r)


# ## Step 4: When you are ready, let's export this
#    1. Open terminal
#    2. Change into course, module6, practices folder
#    3. Convert to a script: `jupyter-nbconvert --to script Google_NoSQL_API_Lab.ipynb`
#     ```
#         [NbConvertApp] Converting notebook Google_NoSQL_API_Lab.ipynb to script
#         [NbConvertApp] Writing 2177 bytes to Google_NoSQL_API_Lab.py
#     ``` 
# #### Move the generated script using `scp` or copy and paste techniques to get it to your VM.

# ## Step 5: Run the your code in the Google VM instance
#  * Your output should be similar to the screenshot
#  
#  
#  
#  ![nosql-python.png](../images/nosql-python.png)

# ## Step 6: SUBMISSION
# * Add a screenshot like the one shown above in the `step 5` for the lab submission
# 
# 
# ![GoogleNoSql.jpg MISSING](GoogleNoSql.jpg)
# 

# # Complete the Clean Up step to remove your NoSQL resource
