import tweepy
#from tweepy import OAuthHandler

#apiKey = "zUgNowBplMt8IpfjQDWng7d6C"
#apiSecret = "jHhTgs22ZGnt9Y9EME5fVaNfIvuixuw9QnWgoA5tfX0yv7JqNT"
#accessToken = "730756597010604032-kZ5f7kphoAjhtnNaFIGRVmrMTvJ6ocW"
#accessTokenSecret = '4dfBZ00HzVVcTLJ1sWjH9GrIcDA5lActNkC2pAmMPwtmL'

auth = tweepy.OAuthHandler('zUgNowBplMt8IpfjQDWng7d6C', 'jHhTgs22ZGnt9Y9EME5fVaNfIvuixuw9QnWgoA5tfX0yv7JqNT')
auth.set_access_token('730756597010604032-kZ5f7kphoAjhtnNaFIGRVmrMTvJ6ocW', '4dfBZ00HzVVcTLJ1sWjH9GrIcDA5lActNkC2pAmMPwtmL')
api = tweepy.API(auth)

for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text) 
    
#def process_or_store(tweet):
#    print(json.dumps(tweet))


##streams tweets and saves to file

#from tweepy import Stream
#from tweepy.streaming import StreamListener
# 
#class MyListener(StreamListener):
# 
#    def on_data(self, data):
#        try:
#            with open('python.json', 'a') as f:
#                f.write(data)
#                return True
#        except BaseException as e:
#            print("Error on_data: %s" % str(e))
#        return True
# 
#    def on_error(self, status):
#        print(status)
#        return True
# 
#twitter_stream = Stream(auth, MyListener())
#twitter_stream.filter(track=['#python'])