#!/usr/bin/env python3

import config
from twitchapi import TwitchAPI

twitch = TwitchAPI(config.client_id, config.oauth_chat, config.channel, config.access_token)
user = 'akimrx'  # insert real twitch username

if __name__ == '__main__':
    print('get_chatters_list: ', twitch.get_chatters_list())
    print('\nget_viewers_list: ', twitch.get_viewers_list())
    print('\nget_user_id: ', twitch.get_user_id(user))
    print('\nget_user: ', twitch.get_user(user))
    print('\ncheck_user_follow: ', twitch.check_user_follow(user))
    print('\nget_follow_time: ', twitch.get_follow_time(user))
    print('\nstream_uptime: ', twitch.stream_uptime())
    print('\nchange_title: ', twitch.change_title('TEST API'))
    print('\nget_title: ', twitch.get_title())
    print('\nchange_category: ', twitch.change_category('Science & Technology'))
    print('\nget_category: ', twitch.get_category())
    print('\nget_subs_count: ', twitch.get_subs_count())
    print('\nget_subs_list: ', twitch.get_subs_list())
    print('\nexport_subs: ', twitch.export_subs())
    print('\nget_viewers_count: ', twitch.get_viewers_count())
    print('\nget_followers_list + export : ', twitch.get_followers_list())

