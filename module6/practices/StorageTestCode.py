#!/usr/bin/env python
# coding: utf-8

# # Some Practice to set up VM tools and Python write some code
# 
# **NOTE**: For this practice, you will work in a Preemptible micro VM.  
# 
# **NOTE**: When you are done, use the "Stop" function from the console on the VM instead of the "Delete" function.
#  * Then you can restart the VM for the exercise.
# 

# ## Installing Python Setup Tools
# 
# ### Check type of Linux at VM command line (from SSH Shell)
#   * `uname -a`
#   
# #### Output should look similar to:
# ```
# Linux instance-1 4.9.0-8-amd64 #1 SMP Debian 4.9.130-2 (2018-10-27) x86_64 GNU/Linux
# ```
#  * Note, we see _Debian_
# 
# 
# ### Following PIP install instructions for Debian
# 
# https://packaging.python.org/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers
# 
# 
# ### Installing Google Cloud Python Interface
#   * `pip3 install google-cloud`
#   
# ### Install git
#   * `sudo apt-get install git`
# 
# ### Clone down the GCP Python Docs Samples
#  `git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git`
#   
# #### Output may look like:
# ```
# Collecting google-cloud
#   Downloading https://files.pythonhosted.org/packages/ba/b1/7c54d1950e7808df06642274e677dbcedba57f75307adf2e5ad8d39e5e0e/google_cloud-0.34.0-py2.py3-none-any.whl
# Installing collected packages: google-cloud
# Successfully installed google-cloud-0.34.0
# ```

# 
# #### Set up Virtual Environment
#  * See: https://cloud.google.com/python/setup
#    * Section: **Installing and using virtualenv**
#    * Remember we are using `pip3` not `pip` because of previous steps.
#    
# #### Deviation from google instructions: Launch the VirtualEnvironment
#  * `python3 -m virtualenv env`
# 
# 
# You should see the virtual environment prompt change:
# ```
# instance-1:~$ source env/bin/activate
# (env) grantscott_phd@instance-1:~$ 
# ```
# 
# #### In your virtual environments, move into the samples for storage/api
#  * `cd python-docs-samples/storage/api/`
#  
# #### Make sure the requirements are installed
#  * `pip3 install -r requirements.txt`

# 
# ---
# 
# # Programmatic Access to GCP Storage Buckets
# 
# ## Bucket Help From:
# 
# https://cloud.google.com/storage/docs/object-basics
# 
# https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/storage/cloud-client
# 
# https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/storage/api
# 
# 
# ## Review the Readme for the list of relevant example code nuggets.
# 
# Example: **list_objects.py**
# ```
# python3 list_objects.py dsa_mini_project_scottgs{
#   "name": "dsa_mini_project_scottgs",
#   "id": "dsa_mini_project_scottgs",
#   "kind": "storage#bucket",
#   "selfLink": "https://www.googleapis.com/storage/v1/b/dsa_mini_project_scottgs",
#   "metageneration": "1",
#   "etag": "CAE=",
#   "updated": "2017-12-09T17:25:58.610Z",
#   "storageClass": "MULTI_REGIONAL",
#   "projectNumber": "684237336060",
#   "timeCreated": "2017-12-09T17:25:58.610Z",
#   "location": "US"
# }
# [
#   {
#     "name": "my_file_1",
#     "contentType": "text/plain",
#     "size": "15"
#   },
#   {
#     "name": "my_file_2",
#     "contentType": "text/plain",
#     "size": "21"
#   }
# ]
# ```

# ### Setting up machine-to-machine access
# 
# The Google Cloud Python interface allows python scripts to interact with the GCP services and resources.
# 
# https://googleapis.github.io/google-cloud-python/
# 
# If you desire to interact with the cloud services and resources from a computer such as your laptop or the MU DSA Jupyter environment, you will need to generate the application default login configuration file.
# 
# https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login
# 
# **NOTE:** If you are on a GCloud VM, you will see this is not necessary.
# 
#  * `gcloud auth application-default login`
#  
# #### Output approximately:
# ```
# You are running on a Google Compute Engine virtual machine.
# The service credentials associated with this virtual machine
# will automatically be used by Application Default
# Credentials, so it is not necessary to use this command.
# ```
# 
# ##### The next cell is an example of what is necessary for non-GCP servers
# 
# Update the next line!  Requires you uploaded the JSON file for Service Account Auth
#MY_USERID = 'lcmhng'
# /home/scottgs/.config/gcloud/application_default_credentials.json
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/" + MY_PAWPRINT + "/.config/gcloud/application_default_credentials.json"

# 
# ### These functions are from the Github demo repo
# 
# Please give these cells a read through... and as you do, move them to a file in your virtual machine, such as 
#   * `my_gcp_storage_test.py`
#   
# Alternatively, see the Notebook python script extraction example at the bottom.

# In[1]:


import os
from google.cloud import storage
## Change to your own project name
PROJECT='lcmhng-mu-dsa'


# In[ ]:


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)
        


# In[ ]:


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


# In[ ]:


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


# In[ ]:


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))



# In[ ]:


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print('Blob {} deleted.'.format(blob_name))


# In[ ]:


# Bucket Name:
my_bucket_name = 'dsa_mini_project_lcmhng'

list_blobs(my_bucket_name)


# In[ ]:


upload_as_blob(my_bucket_name, "This is my data", 'my_file_1')

list_blobs(my_bucket_name)


# In[ ]:


upload_as_blob(my_bucket_name, "This is my other data", 'my_file_2')


# In[ ]:


list_blobs(my_bucket_name)


# In[ ]:


def read_blob(bucket_name, source_blob_name):
    """Downloads a blob from the bucket and returns content in bytearray"""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    return blob.download_as_bytes()


read_blob(my_bucket_name,'my_file_2')


# In[ ]:


def read_blob_as_string(bucket_name, source_blob_name):
    """Downloads a blob from the bucket and returns content in string"""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    return blob.download_as_bytes().decode("utf-8") 


myContent_Back = read_blob_as_string(my_bucket_name,'my_file_2')
print(myContent_Back)


# #### When you are ready, let's export this
#  1. Open terminal
#  2. Change into course, module6, practices folder
#  3. Convert to a script: `jupyter-nbconvert --to script StorageTestCode.ipynb`
# ```
# [NbConvertApp] Converting notebook StorageTestCode.ipynb to script
# [NbConvertApp] Writing 4740 bytes to StorageTestCode.py
# ```
# 
# #### Move the generated script using `scp` or copy and paste techniques to get it to your VM.
