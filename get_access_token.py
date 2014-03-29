#provde the authorization code manually as a single arugment to this script to get the access token. 
#Example call: 
#python get_access_token.py "pasteinauthorizationcode"

import requests
import sys
import json as js

if len(sys.argv) != 2: #first element is script name. 
    sys.exit("Aborting. You must provide authorization api code as a single argument")
else:
    auth_code = sys.argv[1]


execfile('token/client.txt')

tok_url = "https://www.box.com/api/oauth2/token"

d = {'grant_type': "authorization_code",
     'code': auth_code,
     'client_id': cid,
     'client_secret': cpw
}

r = requests.post(tok_url,data=d) #data is for posts, #params is for get
resp = r.json()
print(resp)
#now save to file this output. 
with open('token/access_token.json','w') as f:
    f.write(js.dumps(resp))
