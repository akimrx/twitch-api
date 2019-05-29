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
