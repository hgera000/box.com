import requests
import sys,os
import json as js

#if len(sys.argv) != 2: #first element is script name. 
#    sys.exit("Aborting. You must provide the file name of the token being refreshed (saved as json).")
#else:
#    fname = sys.argv[1]
fname = 'token/access_token.json'
tok_url = "https://www.box.com/api/oauth2/token"
execfile('token/client.txt')


#load the existing token that needs to be refreshed (saved in get_access_token.py)
j = js.loads(file(fname,'r').read())

print(j)

d = {'grant_type': "refresh_token",
     'refresh_token': j['refresh_token'],
     'client_id': cid,
     'client_secret': cpw
}

r = requests.post(tok_url,data=d) #data is for posts, #params is for get
resp = r.json()
print(resp)
#now save to file this output.
#this will overwrite previously saved token. 
with open('token/access_token.json','w') as f:
    f.write(js.dumps(resp))
