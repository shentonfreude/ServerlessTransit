
import twitter
import os
import boto3


DYNAMO_DB_TABLE   = 'serverless-transit'
TRANSIT_AUTHOROTY = 'WMATA'
SEARCH_KEYWORDS = ['metrorailinfo', 'wmata' ,'unsuckdcmetro' ,'rushminus']
BAD_IDENTIFIERS = ['delay','delays', 'crowded', 'bad', 'full', 'incident']
LINES           = ['red', 'silver' , 'blue' , 'yellow' , 'green' , 'bl' , 'or' , 'sv']

def lambda_handler(event, context):
   dynamodb = boto3.client('dynamodb' , region_name='us-west-2')
   tweets = get_tweets()
   for tweet in tweets:
      bad_identifier = is_it_bad_tweet(tweet)
      if bad_identifier:
         print(tweet.full_text)
         lines = extract_lines(tweet)
         print("Founded lines: {0}".format(lines))
         if len(lines) > 0 :
            for line in lines:
               dynamodb.put_item(TableName=DYNAMO_DB_TABLE, Item={ "pk": { "S": "report:"+ TRANSIT_AUTHOROTY+ ":" + line },
               "report_source": { "S": "twitter:@" + tweet.user.screen_name }, "report_text": { "S":  tweet.full_text }, "sk": { "S": tweet.created_at },
               "status": { "S": bad_identifier }, "transit_authority": { "S": TRANSIT_AUTHOROTY }, "transit_line": { "S": line  }, "transit_station": { "S": "ballston" } })

            
            


def extract_lines(tweet):
   results = []
   for line in LINES:
      if line in tweet.full_text.lower():
         results.append(line)
         
   return results
         
def is_it_bad_tweet(tweet):
   for bad_identifier in BAD_IDENTIFIERS:
         if bad_identifier in tweet.full_text.lower():
            return bad_identifier
            
   return False
   
   
   
def get_tweets():
   api = twitter.Api(consumer_key=os.environ['consumer_key'],
                  consumer_secret=os.environ['consumer_secret'],
                  access_token_key=os.environ['access_token'],
                  access_token_secret=os.environ['access_token_secret'])
   query=''
   for i in range(len(SEARCH_KEYWORDS)):
      query += SEARCH_KEYWORDS[i]
      if i!=len(SEARCH_KEYWORDS)-1:
         query +=' OR '
   results = api.GetSearch(raw_query="q={0}&result_type=recent&count=99".format(query))
   return results
