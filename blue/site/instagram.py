import requests
import json
import math
import time
import datetime
import collections

client_secret = " "
client_id = " "
access_token = " "

ACCESS_TOKEN = "BLAHBLAH"
endpointsLookUp = {
    "search_user": "https://api.instagram.com/v1/users/search?q=%s&access_token=%s" + ACCESS_TOKEN,
    "hash_tag": "https://api.instagram.com/v1/tags/%s/media/recent?access_token=" + ACCESS_TOKEN,
    "user_follows": "https://api.instagram.com/v1/users/self/follows?access_token=" + ACCESS_TOKEN,
    "media_info": "https://api.instagram.com/v1/users/%s/media/recent/?access_token=" + ACCESS_TOKEN + "&count=33"}


class USER(object):
    """
    from instagram import API, client_id,  client_secret, access_token
    user = API(client_id, client_secret, access_token)

    call it as
    user = API(client_id, client_secret, access_token)
    user.search_user("champagnepapi")
    user.search_hash_tag("filter")
    """
    def __init__(self, client_id, client_secret, access_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.search_url = None
        self.hash_tag_url = None
        self.user_id_url = None
        self.user_input = None
        self.id = None
        self.profile_url = None
        self.user_search_data = None

    def search_user(self, user_input):
        self.user_input = user_input
        self.search_url = "https://api.instagram.com/v1/users/search?q={}&access_token={}".format(user_input, self.access_token)
        self.user_id_url = "https://api.instagram.com/v1/users/{}/?access_token={}".format(user_input, self.access_token)
        self.user_search_data = requests.get(self.search_url)
        if not (self.user_search_data.json()['data']):
            print "Error searching for your user"  # replace this with raise / test purposes only
        else:
            print "Found something"
        return self.user_search_data

    def search_hash_tag(self, hash_tag):
        self.hash_tag_url = "https://api.instagram.com/v1/tags/{}/media/recent?access_token={}".format(hash_tag, self.access_token)
        return requests.get(self.hash_tag_url)

    def user_id(self):
        search_results = self.user_search_data.json()
        for item in search_results['data']:
            if item['username'] == self.user_input.lower():
                self.id = item['id']
                return self.id

    def profile_data(self):
        self.profile_url = "https://api.instagram.com/v1/users/{}/?access_token={}".format(self.user_id, self.access_token)
        return requests.get(self.profile_url)




