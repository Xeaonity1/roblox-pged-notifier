import time, datetime
import ctypes, requests
from threading import Thread

#config
threadc = 100
webhooks = [
    'webhook'
]
sleep_time = 60 * 30

#vars
cycle = 0
lastonline = {}

def thread():
    global done
    req = requests.Session()
    while db:
        try:
            line = db.pop()
            #username, userid = line.split(':',1)
            username, userid, email = line.split(':', 2)
            year = req.get(f'https://api.roblox.com/users/{userid}/onlinestatus', timeout=5).json()['LastOnline'].split('-')[0]
            if username in lastonline:
                if year != lastonline[username] and int(year) >= 2021:
                    print(username, userid)
                    for webhook_url in webhooks:
                        requests.post(webhook_url, json={
                            'embeds' : [{
                                'color' : 40959,
                                'title' : f'Some noob got pged',
                                'url': f'https://www.roblox.com/users/{userid}/profile',
                                'timestamp' : f'{datetime.datetime.now().astimezone()}',
                                'thumbnail' : {
                                    'url' : requests.get(f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={userid}&size=150x150&format=png').json()['data'][0]['imageUrl']
                                },
                                'fields' : [
                                    {
                                        'name' : 'Username',
                                        'value' : username,
                                        'inline' : True
                                    },
                                    {
                                        'name' : 'UserID',
                                        'value' : userid,
                                        'inline' : True
                                    },
                                    {
                                        'name' : 'Email',
                                        'value' : email,
                                        'inline' : False
                                    },
                                    {
                                        'name': 'Previous lastonline',
                                        'value': lastonline[username],
                                        'inline': False
                                    }
                                ],
                                'footer' : {
                                    'text' : 'idiocrasy'
                                }            
                            }]
                        })
            lastonline[username] = year
        except Exception as e:
            pass
        done += 1

while 1:
    done = 0
    cycle += 1

    db = open('usernames.txt', 'r', errors='ignore').read().splitlines()
    total = len(db)

    for i in range(threadc):
        Thread(target=thread).start()

    for i in range(sleep_time):
        time.sleep(1)
        ctypes.windll.kernel32.SetConsoleTitleW(f'PGed Account Notifier | Cycle: {cycle} | Progress: {done}/{total} | Sleeping: {i}/{sleep_time}')
