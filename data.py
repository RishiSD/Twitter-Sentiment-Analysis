import tweepy
from Tweet import Tweet
from auth import twit_auth_handler


class TwitterMain:

    def __init__(self):

        self.api = twit_auth_handler()

    def get_tweet_html(self, id):

        oembed = self.api.get_oembed(id=id, hide_media=True, hide_thread=True)
        return oembed['html'].strip('\n')

    def get_trends(self, text_query):
        
        tt_buff = list()
        embed_list = list()
        for t in tweepy.Cursor(self.api.search, q = text_query + ' -filter:retweets' , lang='en').items(5):
            embed_twit = self.get_tweet_html(t.id)
            tweet = Tweet(text_query, str(t.id), t._json["lang"], t._json["text"], embed_twit)
            embed_list.append(embed_twit)
            tt_buff.append(tweet)

        Tweet.save_all_to_db(tt_buff)

        return embed_list
