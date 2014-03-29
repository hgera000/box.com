import requests
import sys, os
import json

#Upload a local file to a box.com folder
#Takes three arguments: 1. filepath to be uploaded 2. destination folder ID 3. existing file id
#Example call:
#$ python ~/path_to_file.file.txt 1234567 7654321


if len(sys.argv) != 4: #first element is script name. 
    sys.exit("Aborting. You must provide in this order: filename path and folder id and existing file id (so it can be replaced if already exists)")
else:
    fname = sys.argv[1]
    fid = sys.argv[2]
    exist_id = sys.argv[3]

data = {"parent_id": fid}
files = {"filename": open(fname,'rb') } #fid is name of folder in box you are uploading to. fname is name of file to upload (given as argument). 

access_token = json.loads(open('../token/access_token.json').read())['access_token']

header = {'Authorization':'Bearer %s' % access_token}

upload_url = "https://upload.box.com/api/2.0/files/%s/content"

resp = requests.post(upload_url % exist_id, headers=header,data=data,files=files)
print("api call, response code: %s" % resp.status_code)
print(resp.text)


