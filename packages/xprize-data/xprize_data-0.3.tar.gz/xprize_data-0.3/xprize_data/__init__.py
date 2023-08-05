# Pip install packages
import os, sys
#!{sys.executable} -m pip install azure-storage  
#!{sys.executable} -m pip install pyarrow 
#!{sys.executable} -m pip install pandas 
#!{sys.executable} -m pip install ipywidgets

import pandas as pd
from IPython.display import display, HTML
from IPython.display import clear_output
from azure.storage.blob import BlockBlobService
import ipywidgets as widgets
import requests


def getDatasets(apiKey):

    #test API Key: ogOXCDpGp5xCAHBezgaIUsHf2rWXM3k3PgOEO9VlxySb3U3WEpQztA==
    
    clear_output()

    # Azure storage access info
    azure_storage_account_name = "datacommons"
    azure_storage_sas_token = r"sv=2018-03-28&ss=b&srt=sco&sp=rl&se=2019-07-24T06:38:59Z&st=2019-07-22T22:38:59Z&spr=https&sig=f6RqmXdz4fat8QCkcIYZwX%2F8WOTd4K7yu1r%2Fb2pp1A8%3D" #r"sv=2018-03-28&ss=b&srt=sco&sp=rwdlac&se=2019-07-24T06:14:23Z&st=2019-07-22T22:14:23Z&spr=https&sig=e9Ux9P0CUQiXQHckHUjseZ3CCkd%2FIL7Q7gGZqcFVDgg%3D"
    container_name = "public"
    folder_name = "" #file name starts with

    #get SAS token
    # data to be sent to api
    url = 'https://functions-pop.azurewebsites.net/api/blob-sas-token-generator?code=' + apiKey
    payload = {'container':'public', 'blobname':'', 'permissions':'Read,List'}
    headers = {'content-type': 'application/json'}

    resp = requests.request('POST', url=url, json=payload,headers=headers)
    if resp.status_code != 200:
        raise Exception("Cannot retrieve SAS token")

    data = resp.json()
    token = data['token']
    azure_storage_sas_token = token[1:]

    #button = widgets.Button(description="List Files")
    #output = widgets.Output()

    #display(button, output)

    #def on_files_button_clicked(b):
    #    with output:

    if azure_storage_account_name is None or azure_storage_sas_token is None:
        raise Exception("Provide your specific name and key for your Azure Storage account")

    #next_marker = None
    blob_service = BlockBlobService(account_name = azure_storage_account_name, sas_token = azure_storage_sas_token,)
    blobs = blob_service.list_blobs(container_name) 
    sorted_blobs = sorted(list(blobs), key=lambda e: e.name, reverse=False)


    # Calling DataFrame constructor on list
    print('Files found:')
    files = {'File Name': [], 'Size(MB)':[]}
    i=1
    for blob in sorted_blobs:
        if blob.name.startswith(folder_name) and not blob.name.endswith('_JSON'):
            #mylist.append(blob.name)
            length = BlockBlobService.get_blob_properties(blob_service,container_name,blob.name).properties.content_length
            files['File Name'].append(blob.name)
            files['Size(MB)'].append(length/1048576) #convert to MB
            print('Files found:', end =" ")
            print(i)
            i = i+1
            clear_output(wait=True)  
            #break


    df = pd.DataFrame(files)
    #display(HTML(df.to_html()))
    return (df)
