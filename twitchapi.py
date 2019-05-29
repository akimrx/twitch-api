import csv
import json
import time
import requests
import threading
import logging
from datetime import datetime


# Wrapper for new threads (async)
def thread(func):
    def wrapper(*args, **kwargs):
        current_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        current_thread.start()
    return wrapper


# User-friendly output
class Wrappers:
    # Resolve seconds to good values
    def seconds_raw(self, seconds, granularity=2):
        result = []
        intervals = (
            ('years', 31104000),
            ('months', 2592000),
            ('weeks', 604800),
            ('days', 86400),
            ('hours', 3600),
            ('minutes', 60),
            ('seconds', 1),
        )
        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append(f"{value} {name}")
        return ', '.join(result[:granularity])

    # Resolve minutes to good values
    def minutes_raw(self, minutes, granularity=2):
        result = []
        intervals = (
            ('hours', 60),
            ('minutes', 1),
        )
        for name, count in intervals:
            value = minutes // count
            if value:
                minutes -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append(f"{value} {name}")
        return ', '.join(result[:granularity])


class TwitchAPI:
    wrappers = Wrappers()
    followers = {}

    def __init__(self, client_id, oauth_chat, channel, access_token):
        self.client_id = client_id
        self.channel = channel
        self.oauth = oauth_chat
        self.access_token = access_token
        self.channel_id = self.get_user_id(self.channel)

    # Get users list from twitch IRC chat
    def get_chatters_list(self):
        url = f'http://tmi.twitch.tv/group/user/{self.channel}/chatters'
        req = requests.get(url)
        res = json.loads(req.text)
        if req.status_code != 200:
            logging.warning(res)
        else:
            broadcaster = res["chatters"]["broadcaster"]
            moderators = res["chatters"]["moderators"]
            viewers = res["chatters"]["viewers"]
            vips = res["chatters"]["vips"]
            merged_list = list(set(broadcaster + moderators + viewers + vips))
            return merged_list

    # Get users list from twitch IRC chat (only vips & viewers)
    def get_viewers_list(self):
        url = f'http://tmi.twitch.tv/group/user/{self.channel}/chatters'
        req = requests.get(url)
        res = json.loads(req.text)
        if req.status_code != 200:
            logging.error(res)
        else:
            viewers = res["chatters"]["viewers"]
            vips = res["chatters"]["vips"]
            merged_list = list(set(viewers + vips))
            return merged_list

    # Login to User ID resolve
    def get_user_id(self, user):
        url = f'https://api.twitch.tv/kraken/users?login={user}'
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self.client_id
            }
        req = requests.get(url, headers=headers)
        res = json.loads(req.text)
        if req.status_code != 200:
            logging.error(res)
        else:
            user_id = res["users"][0]["_id"]
            return user_id

    # Get twitch user info
    def get_user(self, user):
        url = f'https://api.twitch.tv/kraken/users?login={user}'
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self.client_id
            }
        req = requests.get(url, headers=headers)
        res = json.loads(req.text)
        if req.status_code != 200:
            logging.error(res)
        else:
            return res['users'][0]

    # Check follow user to channel
    def check_user_follow(self, user):
        user_id = self.get_user_id(user)
        url = f'https://api.twitch.tv/kraken/users/{user_id}/follows/channels/{self.channel_id}'
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self.client_id
            }
        req = requests.get(url, headers=headers)
        res = json.loads(req.text)
        if req.status_code == 200:
            if res['created_at']:
                return self.get_user(user)

    # Wrapped user follow age
    def get_follow_time(self, user):
        user_id = self.get_user_id(user)
        url = f'https://api.twitch.tv/kraken/users/{user_id}/follows/channels/{self.channel_id}'
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self.client_id
            }
        req = requests.get(url, headers=headers)
        res = json.loads(req.text)
        if req.status_code == 404:
            return res['message']
        elif req.status_code == 200:
            data = res['created_at']
            cur_time = datetime.utcnow()
            follow_time = datetime.strptime(data, '%Y-%m-%dT%H:%M:%Sz')
            diff = int((cur_time - follow_time).total_seconds())
            return self.wrappers.seconds_raw(diff, 2)
        else:
            logging.warning(res)

    # Wrapped elapsed time after stream start
    def stream_uptime(self):
        url = f'https://api.twitch.tv/kraken/streams/{self.channel_id}'
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self.client_id
            }
        req = requests.get(url, headers=headers)
        res = json.loads(req.text)
        if req.status_code != 200:
            logging.warning(res)
        else:
            if res['stream'] is not None:
                data = res['stream']['created_at']
                cur_time = datetime.utcnow()
                up_time = datetime.strptime(data, '%Y-%m-%dT%H:%M:%Sz')
                uptime = cur_time - up_time
                return str(uptime)[:-10]

    # Stream title changer
    def change_title(self, title):
        url = f'https://api.twitch.tv/kraken/channels/{self.channel_id}'
        headers = {
            'Client-ID': self.client_id,
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Authorization': f'OAuth {self.access_token}',
            'content-type': 'application/json'
            }
        data = {
            'channel': {
                'status': title
                }
            }
        req = requests.put(url, data=json.dumps(data), headers=headers)
        res = json.loads(req.text)
        if req.status_code != 200:
            logging.warning(res)
        else:
            data = req.json()
            new_title = data['status']
            logging.info(f'Title changed: {new_title}')
            return new_title

    # Get current stream title
    def get_title(self):
        url = f'https://api.twitch.tv/kraken/channels/{self.channel_id}'
        headers = {
            'Client-ID': self.client_id,
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Authorization': f'OAuth {self.access_token}',
            'content-type': 'application/json'
            }
        req = requests.get(url, headers=headers)
        res = json.loads(req.text)
        if req.status_code != 200:
            logging.warning(res)
        else:
            data = req.json()
            title = data['status']
            logging.info(f'Title: {title}')
            return title

    # Stream category changer
    def change_category(self, category):
        url = f'https://api.twitch.tv/kraken/channels/{self.channel_id}'
        headers = {
            'Client-ID': self.client_id,
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Authorization': f'OAuth {self.access_token}',
            'content-type': 'application/json'
            }
        data = {
                'channel': {
                    'game': category
                    }
                }
        req = requests.put(url, data=json.dumps(data), headers=headers)
        res = json.loads(req.text)
        if req.status_code != 200:
            logging.warning(res)
        else:
            data = req.json()
            new_game = data['game']
            logging.info(f'Game changed: {new_game.title()}')
            return new_game.title()

    # Get current stream category
    def get_category(self):
        url = f'https://api.twitch.tv/kraken/channels/{self.channel_id}'
        headers = {
            'Client-ID': self.client_id,
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Authorization': f'OAuth {self.access_token}',
            'content-type': 'application/json'
            }
        req = requests.get(url, headers=headers)
        res = json.loads(req.text)
        if req.status_code != 200:
            logging.warning(res)
        else:
            data = json.loads(req.text)
            logging.info(f'Current category: {data["game"].title()}')
            return data['game']

    # Get active subscribers count
    def get_subs_count(self):
        url = f'https://api.twitch.tv/helix/subscriptions?broadcaster_id={self.channel_id}'
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Authorization': f'Bearer {self.access_token}',
            'Client-ID': self.client_id
            }
        req = requests.get(url, headers=headers)
        res = json.loads(req.text)
        if req.status_code != 200:
            logging.warning(res)
        else:
            count = len(res['data'])
            return count

    # Get subscribers list
    def get_subs_list(self):
        url = f'https://api.twitch.tv/helix/subscriptions?broadcaster_id={self.channel_id}'
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Authorization': f'Bearer {self.access_token}',
            'Client-ID': self.client_id
            }
        req = requests.get(url, headers=headers)
        res = json.loads(req.text)
        if req.status_code != 200:
            logging.warning(res)
        else:
            users = res['data']
            subscribers = []
            for username in users:
                sub = username['user_name']
                subscribers.append(sub.lower())
            return subscribers

    # Export subscribers list to CSV file
    def export_subs(self):
        try:
            with open('subscribers.csv', 'w', encoding='utf-8', newline='') as outfile:
                for name in self.get_subs_list():
                    row = name + '\n'
                    outfile.write(row)
            outfile.close()
            logging.info('File subscribers.csv created')
            return 'Subcribers exported to subsribers.csv'
        except Exception as e:
            logging.warning(f'Failed create subscribers.csv: {e}')

    # Get stream viewers count
    def get_viewers_count(self):
        url = f'https://api.twitch.tv/kraken/streams/{self.channel_id}'
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self.client_id
            }
        req = requests.get(url, headers=headers)
        res = json.loads(req.text)
        if req.status_code != 200:
            logging.warning(res)
        else:
            if res['stream'] is not None:
                data = res['stream']['viewers']
                return data

    # Exclusive thread followers list generator
    @thread
    def get_followers_list(self):
        try:
            first_url = f'https://api.twitch.tv/helix/users/follows?to_id={self.channel_id}&first=100'
            headers = {
                'Client-ID': self.client_id,
                'content-type': 'application/json'
            }
            # first 100 followers without pagination
            r = requests.get(first_url, headers=headers)
            first_data = json.loads(r.text)
            for follower in first_data['data']:
                self.followers[follower['from_name']]=follower['from_id']
            pagination = first_data['pagination']['cursor']
            url = f'https://api.twitch.tv/helix/users/follows?to_id={self.channel_id}&first=100&after='
            # second 100 followers with pagination
            r = requests.get(url + pagination, headers=headers)
            data = json.loads(r.text)
            for follower in data['data']:
                self.followers[follower['from_name']]=follower['from_id']
            if 'cursor' in data['pagination']:
                cursor = data['pagination']['cursor']  
                # third 100 followers with pagination
                r = requests.get(url + cursor, headers=headers)
                new_data = json.loads(r.text)
                if 'cursor' in new_data['pagination']:
                    new_cursor = new_data['pagination']['cursor']
                    for follower in new_data['data']:
                        self.followers[follower['from_name']]=follower['from_id']
                    while True:
                        time.sleep(2)
                        # sequential requests with pagination
                        req = requests.get(url + new_cursor, headers=headers)
                        res = json.loads(req.text)
                        if 'cursor' in res['pagination']:
                            new_cursor = res['pagination']['cursor']
                            for follower in res['data']:
                                self.followers[follower['from_name']]=follower['from_id']
                        else:
                            break
            logging.info('Dict Followers created')
        except Exception as e:
            logging.warning(f'Error in followers-get: {e}')
        finally:
            self.export_followers()

    # Export followers list to CSV file
    def export_followers(self):
        with open('followers.csv', 'w', encoding='utf-8', newline='') as outfile:
            wr = csv.writer(outfile)
            for user in self.followers.keys():
                username = user
                user_id = self.followers[username]
                row = username, user_id
                wr.writerow(row)
            outfile.close()
            logging.info(f'{len(self.followers)} followers saved to followers.csv')
        return 'Followers saved to followers.csv'
