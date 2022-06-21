import csv
import yaml
import tweepy
import pprint
import json
from yaml.loader import SafeLoader


class TwitterScraper():
    def __init__(self, csv_to_read, yaml_to_read):
        self.csv_to_read = csv_to_read
        self.yaml_to_read = yaml_to_read
        self.wordlist = []

        self.auth_accounts = []

        # for secrets from config
        self.cons_key = ''
        self.cons_secret = ''
        self.acc_token = ''
        self.acc_token_secret = ''

        # for twitter auth and client retrieve
        self.auth = None
        self.client = None

        # for yaml loading
        self.yaml_data = {}

        # for tweets retrieve
        self.url = "https://api.twitter.com/2/tweets/search/recent?max_results=20&query=from%3A****&user.fields=profile_image_url%2Curl%2Cusername%2Cname&tweet.fields=created_at&expansions=author_id"
        self.payload = {}
        self.headers = {
            'Authorization': '',
        }
        self.bearer_token = ''

        # data for storing tweets
        self.users_data = {}
        self.temp_str = ''

        # date conversion
        self.date = ''
        self.date_str = ''

        # for sending json
        self.send_data = []

        # for filter news
        self.filtered_list = []
        self.to_json_filtered_list = []

    def read_from_csv(self):
        with open(self.csv_to_read, 'r') as file:
            reader = csv.reader(file)
            self.wordlist = [element for row in reader for element in row]

    def load_yaml_file(self):
        with open(self.yaml_to_read) as f:
            self.yaml_data = yaml.load(f, Loader=SafeLoader)

    def unpack_yaml(self):
        self.cons_key = self.yaml_data['resources']['secrets']['cons_key']
        self.cons_secret = self.yaml_data['resources']['secrets']['cons_secret']
        self.acc_token = self.yaml_data['resources']['secrets']['acc_token']
        self.acc_token_secret = self.yaml_data['resources']['secrets']['acc_token_secret']
        self.bearer_token = self.yaml_data['resources']['secrets']['bearer_token']
        self.auth_accounts = self.yaml_data['resources']['authorized_account_ids']

    def get_twitter_auth(self):
        # authenticating to Twitter
        try:
            self.auth = tweepy.OAuthHandler(self.cons_key, self.cons_secret)
            self.auth.set_access_token(self.acc_token, self.acc_token_secret)
        except KeyError as kerr:
            print(kerr)

    def get_twitter_client(self):
        self.client = tweepy.API(self.auth, wait_on_rate_limit=True)
        return self.client

    def get_tweets(self, url):
        self.headers['Authorization'] = self.bearer_token
        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        self.temp_str = response.text

    def aggregate_data(self):
        for account_name in self.auth_accounts:
            temp_string = self.url.split("****", 2)
            url = temp_string[0] + account_name + temp_string[1]
            self.get_tweets(url)
            user_data = self.temp_str
            self.users_data[account_name] = user_data

    def filter_alerts(self):
        for value in self.users_data.values():
            temp_dict = json.loads(value)
            self.filtered_list = temp_dict['data']

            temp_dict_list_copy = self.filtered_list.copy()
            for tweet_data in temp_dict_list_copy:
                i = 0
                end_flag = False
                for lemma_word in self.wordlist:
                    i += 1
                    if i == len(self.wordlist):
                        end_flag = True
                    if lemma_word.capitalize() in tweet_data['text'] or lemma_word in tweet_data['text']:
                        break
                    else:
                        if end_flag:
                            self.filtered_list.remove(tweet_data)
                            post_id = tweet_data['id']
                            print(f"Removed: post with: {post_id} and data: {tweet_data['text']}")
                            break
            self.to_json_filtered_list.append(temp_dict)

    def flatten_date(self):
        flatten = self.date.split("T", 1)[0]
        year = flatten[0:4]
        month = flatten[5:7]
        day = flatten[8:10]
        self.date_str = day + "/" + month + "/" + year

    def prepare_json(self):

        for temp_dict in self.to_json_filtered_list:
            author = temp_dict['includes']['users'][0]['name']
            username = temp_dict['includes']['users'][0]['username']
            author_link = "https://twitter.com/" + username
            avatar = temp_dict['includes']['users'][0]['profile_image_url']

            avatar_strip = avatar.split("_normal.jpg", 1)[0]
            avatar_strip = avatar_strip + "_400x400.jpg"
            avatar = avatar_strip

            for alert in temp_dict['data']:
                content = alert['text']
                link = author_link + "/" + "status" + "/" + alert['id']
                self.date = alert['created_at']
                self.flatten_date()
                date_string = self.date_str
                temp_json = {"content": content, "content_images": "[]",
                             "author": author, "author_link": author_link, "username": username,
                             "link": link, "date": date_string, "avatar": avatar}
                self.send_data.append(temp_json)


twitter_obj = TwitterScraper('wordlist.csv', 'config.yaml')
twitter_obj.read_from_csv()
twitter_obj.load_yaml_file()
twitter_obj.unpack_yaml()
twitter_obj.aggregate_data()
twitter_obj.filter_alerts()
twitter_obj.prepare_json()
payload = twitter_obj.send_data