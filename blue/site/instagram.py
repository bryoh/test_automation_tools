import requests
from datetime import datetime
from pprint import pprint as pp
from collections import Counter
import itertools

time_fmt = "%c"  # because time is very important define it here.
# client secret,  id and token seriously need a home
client_secret = ""
client_id = ""
access_token = ""


def request_handler(url, lookup_str=None):
    """"
    returns a whole json dictionary if no lookup_str is provide
    otherwise it returns a dict value whereby the key matches the lookup_str
    """
    request_result = requests.get(url=url)
    if request_result.status_code is not 200:
        print("object not found")
        return request_result

    json_result = request_result.json()
    if lookup_str is not None:
        try:
            ret = json_result[lookup_str]
        except KeyError:
            ret = json_result
            status = str(request_result.status_code)
            print("Key '{}' not found \n url: {} \n response: {}".format(lookup_str, url, status))  # replace with something like an assert
    else:
        ret = json_result
    return ret


class User:
    """
    Base class to store urls, user_id, user search data etc
    urls = User() for when we just want urls formatted with the access toke, client_id and client secret
    drake = User("champagnepapi") for when we want user information + formatted urls
    """

    def __init__(self, username=None, media_id=None):
        self.username = username
        self.media_id = media_id
        if media_id is not None:
            self.media_id_url = "https://api.instagram.com/v1/media/{}?access_token={}".format(self.media_id, access_token)

        if username is not None:
            search_url = "https://api.instagram.com/v1/users/search?q={}&access_token={}".format(username, self.access_token)
            self.user_search_data = request_handler(search_url, "data")[0]  # requests.get(search_url)
            self.user_id = self.user_search_data['id']

            self.user_info_url = "https://api.instagram.com/v1/users/{}/?access_token={}".format(self.user_id, access_token)
            self.recent_media_url = "https://api.instagram.com/v1/users/{}/media/recent/?access_token={}".format(self.user_id, access_token)

            self.user_info_data = request_handler(self.user_info_url, 'data')


class Profile(User):
    """
    gets profile infomation such as total following and followers
    bryoh = Profile("bryoh_15")
    print(bryoh.user_search_data)
    print(bryoh.recent_media_data)
    print(bryoh.followers)
    print(bryoh.following)
    """
    def __init__(self, username):
        User.__init__(self, username)
        self.name = self.user_search_data["full_name"]
        self.bio = self.user_search_data["bio"]
        self.id = self.user_id
        self.profile_picture_link = self.user_search_data["profile_picture"]
        self.website = self.user_search_data["website"]
        self.counts = self.user_info_data["counts"]
        self.followers = self.counts["followed_by"]
        self.follows = self.counts["follows"]
        self.media_total = self.counts['media']
        self.media_recent_data = request_handler(self.recent_media_url, 'data')
        self.media_recent_obj_list = [Media(media_data=obj) for obj in self.media_recent_data]
        self.common_tags = list(itertools.chain(*[Media(media_data=obj).tags for obj in self.media_recent_data]))


class Media(User):
    """
    Gets media info such as date/time, tags, caption,filter, comments count, etc
    Requires the media-id
    """
    def __init__(self, media_id=None, media_data=None):
        if media_id is not None:
            User.__init__(self, media_id=media_id)
            self.media_data = request_handler(self.media_id_url, 'data')
        if media_data is not None:
            self.media_data = media_data
        self.likes = self.media_data["likes"]['count']
        self.attribution = self.media_data["attribution"]
        self.tags = self.media_data["tags"]
        self.images = self.media_data["images"]
        self.comments = self.media_data["comments"]['count']
        self.media_filter = self.media_data["filter"]
        timestamp = self.media_data["created_time"]
        self.created_time = datetime.fromtimestamp(float(timestamp)).strftime(time_fmt)
        self.link = self.media_data["link"]
        self.location = self.media_data["location"]
        self.user_has_liked = self.media_data["user_has_liked"]
        self.users_in_photo = self.media_data["users_in_photo"]
        self.caption = self.media_data["caption"]  # ['text']
        self.media_type = self.media_data["type"]
        self.media_id = self.media_data["id"]
        self.media_user = self.media_data["user"]


def main():
    s = Profile("bryoh_15")
    #g = Profile("champagnepapi")
    #gs = g.followers
    growth = [(obj.created_time, obj.likes ) for obj in s.media_recent_obj_list ]

    pp(Counter(s.common_tags))

if __name__ == "__main__":
    main()


