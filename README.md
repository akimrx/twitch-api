Twitch API Client
=================

Twitch API v5 (kraken) & New Twitch API (helix)

Writed on **Python 3.6.7**

For support, you can join the [Discord Server](https://discordapp.com/invite/8CtkuDZ)

For urgent questions use [Telegram](https://t.me/akimrx)

Usage
==============================================
### Get Client-ID

[Create App on TwitchDev](https://glass.twitch.tv/console/apps)

### Generate OAuth tokens

[OAuth IRC token](https://twitchapps.com/tmi/)

[OAuth Access token (implict)](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/#oauth-implicit-code-flow) with all [scopes](https://dev.twitch.tv/docs/authentication/#scopes)


### Edit config file

* Open `twitch.cfg`
* Insert data into file

Example:
```
[twitch]
account = bot/app-account-username
oauth_chat = oauth:your-token-here
channel = channel-username
access_token = your-acces-oauth-token-here
client_id = your-client-id-here
```

**For test you can run `example-usage.py`**

Methods
=======

### get_chatters_list()
**Action:** Return all users from chat

**Type:** list

**Response:**
```
['iamsorrybot', 'eluri', 'moobot', 'akimrx']
```

### get_viewer_list()
**Action:** Return only viewers and vips from chat

**Type:** list

**Response:**
```
['eluri', 'moobot']
```

### get_user_id(user)
**Action:** Return user id

**Type:** str

**Response:**
```
116410458
```

### get_user(user)
**Action:** Return user info

**Type:** dict

**Response:**
```
{'display_name': 'AKIMRX', '_id': '116410458', 'name': 'akimrx', 'type': 'user', 'bio': '      ', 'created_at': '2016-02-20T10:30:34.241107Z', 'updated_at': '2019-07-22T08:20:36.6368Z', 'logo': 'https://static-cdn.jtvnw.net/jtv_user_pictures/99d68718-ee97-44cd-a75a-c5edd3fa5b7f-profile_image-300x300.jpg'}
```

### check_user_follow(user)
**Action:** Return True or False

**Type:** boolean

**Response:**
```
if follower: True
else: False
```

### get_follow_time(user)
**Action:** Return wrapped follow time for user

**Type:** str

**Response:**
```5 months, 3 weeks```


### stream_uptime()
**Action:** Return stream uptime if stream is live, else return None

**Type:** str

**Response:**
`0:10` or `None`


### change_title(title)
**Action:** Change stream title and return new title

**Type:** str

**Response:**
`TEST API`

### get_title()
**Action:** Return current title

**Type:** str

**Response:**
`TEST API`

### change_category(category)
**Action:** Change stream category and return new category

**Type:** str

**Response:**
`Science & Technology`

### get_category()
**Action:** Return current category

**Type:** str

**Response:**
`Science & Technology`

### get_subs_count()
**Action:** Return subs count

**Type:** int

**Response:**
`23`

### get_subs_list()
**Action:** Return subs count

**Type:** list

**Response:**
`['user1', 'user2', 'user3', 'user99']`

### export_subs()
**Action:** Generate subs list and export to csv

**Type:** csv


### get_viewers_count()
**Action:** Return viewers count if stream is live, else None

**Type:** int

**Response:**
`56`


### get_followers_list()
**Action:** Generate followers list

**Type:** dict


### export_followers()
**Action:** Export followers from get_followers_list to csv

**Type:** csv