import tweepy
from Tweet import Tweet
from auth import twit_auth_handler


class TwitterMain:

    def __init__(self):

        self.api = twit_auth_handler()

    def get_tweet_html(self, id):

        oembed = self.api.get_oembed(id=id, hide_media=True, hide_thread=True)
        return oembed['html'].strip('\n')

    def get_trends(self, text_query, count):
        
        tt_buff = list()
        for t in tweepy.Cursor(self.api.search, q = text_query + ' -filter:retweets' , lang='en').items(count):
            tweet = Tweet(text_query, t.id, t._json["lang"], t._json["text"])
            tt_buff.append(tweet)

        Tweet.save_all_to_db(tt_buff)

        return [self.get_tweet_html(t.tweet_id) for t in tt_buff[:10]]

    @classmethod			
    def get_analysis_data(cls, text_query):
        negative=0
        positive=0
        neutral=0     		
        sentiment_list = Tweet.query.filter_by(tag=text_query).with_entities(Tweet.sentiment).all()
        for i in sentiment_list:
            if i[0] <= -0.31:	
                negative += 1
            elif -0.31 < i[0] < 0.31:
                neutral += 1
            else:
                positive += 1		

        return [negative, positive, neutral]
