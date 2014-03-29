box.com
=======

#Token Setup
0. An app associated with your box.com account first needs to be created through the box developers site: (https://app.box.com/developers/services). Set the redirect URL to be https://127.0.0.1
1. After cloning this repository, create the subfolder box.com/token. This folder will hold your client ID and client Secret, along with access token when generated. Do not make this folder public in any way (for example, never push this folder to github!)
2. Within the subfolder, create a simple text file and call it client.txt containing two lines:
```
cid = "paste in your client id here"
cpw = "paste in your client secret here'
```
Now from your application page, copy the client_id and client_secret and paste them into client.txt. 
3. Now it's time to generate a token. Paste the client_id into the link below, and access the website. 
[Click this link to generate launch box login and generate first authorization code](https://app.box.com/api/oauth2/authorize?response_type=code&client_id=PASTE_CLIENT_ID_HERE&state=security_token%random_string_987654321 "Box.com login") 
4. After logging in and authorizing your app, copy the token from the address bar, and paste it as a single argument as shown below.
```
python get_access_token "pastecodefromlinkabovehere"
```
5. That's it. It is now easy to refresh your applications credentials without any more mucking around. Just run:
```
python refresh_access_token
```

#API Calls
##Monitor Events
1. A script to monitor events on a given folder in box.com. It will print to screen certain 'allowed' or 'disallowed' events as detailed in whitelist.py.
```
python box.com/apicalls/monitor/print_events.py
```
2. The script is designed to be deployed through cron, every workday, say, 9am.

```
0 9 * * 1-5	python ~/box.com/apicalls/monitor/print_events.py
```
##Upload a file
1. This script uploads a local file to your box.com account. Useful for automating backups. 

##Lock files
1. This script locks or unlocks all the files in a given folder (including all the sub folders, and sub-sub folders etc.). 