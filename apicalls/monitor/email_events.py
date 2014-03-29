import requests
import sys,os
import json as js
from datetime import datetime, timedelta, date
from pytz import timezone
import pytz

#Prints to screen a list of allowed and disallowed events
#Designed to be run through cron every day for example. 
#Example call
#python email_events.py


###-----load token and current file & folder dictionary

access_token = js.loads(open('../../token/access_token.json').read())['access_token']
ysp = 0 #js.loads(open('../../token/nsp.json').read())  #ysp = 'yesterdays start position' #or set to zero to get all events

#create whitelist of emails allowed to make changes.
#Also events to monitor are created here.  
execfile('apicalls/monitor/whitelist.py') #create dictionary called whitelist

###------setting up
event_url = "https://api.box.com/2.0/events?stream_position=%s" #defaults to 100 events per call. 
header = {'Authorization':'Bearer %s' % access_token}
pacific = timezone('US/Pacific')
eastern = timezone('US/Eastern')

###--------Initial call to get current stream position
resp = requests.get(event_url % "now", headers=header)
print(resp.status_code)
print(resp.json())
lsp = resp.json()['next_stream_position'] #this is the latest stream position.
nsp = 0 #ysp #can put this at 0 for all, returns first 100 events, and next stream position, or put it as ysp

while nsp < lsp: #loop through all events, stop when get to lsp. 
    resp = requests.get(event_url % nsp, headers=header)
    for e in resp.json()['entries']:
        if e['event_type'] not in events:
            continue; #ignore this event if not in the events dictionary
      
        elif e['created_by']['login'] in whitelist:
            #continue; #now do nothing with allowed events. 
            stdout = 'Allowed event: %s by %s at %s to %s: %s'

        elif e['created_by']['login'] not in whitelist:
            stdout = '!!Disallowed event!!: %s by %s at %s to %s: %s'

        dt = pacific.localize(datetime.strptime(e['created_at'],'%Y-%m-%dT%H:%M:%S-'+e['created_at'].split('-')[-1]))
        dt = datetime.strftime(dt.astimezone(eastern),'%Y-%m-%d %H:%M')
        output = stdout % (e['event_type'],e['created_by']['name'],dt,e['source']['type'],e['source']['name']) 
        print(output.encode('utf-8'))

    nsp = resp.json()['next_stream_position']

#save nsp for tomorrow
with open('../../token/nsp.json','w') as f:
    f.write(js.dumps(nsp))

#Done.     
      
