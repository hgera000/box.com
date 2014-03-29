import requests
import sys, json, os

fid = "12345678" #paste in manually here the folder ID you want to lock. Available from the URL on box.com

d = {"lock": {"expires_at":"2013-01-07"}} # set this to "expires_at":"2013-01-07" to unlock a file, set this to a date in the future, to put an expiration date for the lock.

access_token = json.loads(open('../token/access_token.json').read())['access_token']

header = {'Authorization':'Bearer %s' % access_token}

fold_url = "https://api.box.com/2.0/folders/%s/items?"

lock_url = "https://api.box.com/2.0/files/%s?fields=lock"


#2. Files: for a given folder (fid), list all the files in that folder. 

resp = requests.get(fold_url % fid, headers=header)
print("Initial api call to main folder, response code: %s" % resp.status_code)
files = resp.json()['entries'] 
#files = resp.json()['entries'][0:1] #to test, use [10:11] here to pick only the 11th file say. 

def lock_files(filelist):
    for f in filelist:
        if f['type'] == 'file':
            # r = requests.put(lock_url % f['id'], data = json.dumps(d), headers = header) #if want to use an expiration date or unlock
            r = requests.put(lock_url % f['id'], headers = header) # # to lock files
            if r.status_code!=200:
                sys.exit("Aborting program on file ID %s with status code %s" % (f['name'], r.status_code)) 
            print("Status code %s. File name is %s and lock status '%s'." % (r.status_code, f['name'], r.json()['lock']['type']))
        
        elif f['type'] == 'folder':
            print("Traversing to a new folder: %s" % f['name'])
            resp = requests.get(fold_url % f['id'], headers=header)
            subfiles = resp.json()['entries']
            lock_files(subfiles)


#The actual call to the function. 
lock_files(files)


