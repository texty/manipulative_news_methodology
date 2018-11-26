import requests, re, codecs, json
import pandas as pd
from sqlalchemy import create_engine
from time import sleep

start = pd.to_datetime('now', utc=True).tz_convert('Europe/Kiev')

with open('../psql_engine.txt', 'r') as f:
    psql = create_engine(f.read())

def fb_token():
    '''
    loads credentials from local file and returns requested FB access token
    '''
    with open('my_fb.json') as f:
        auth_credentials = json.load(f)
        
    fb_auth_url = '''https://graph.facebook.com/v2.10/oauth/access_token?client_id={appid}&client_secret={appsecret}&grant_type=client_credentials'''
    token = requests.get(fb_auth_url.format(appid=auth_credentials['appid'],
                                            appsecret=auth_credentials['appsecret'])).json()['access_token']
    return(token)

token = '&access_token=' + fb_token()

sites = pd.read_csv('sites_ids.csv')
fbsites = sites.loc[pd.notnull(sites.fb_id), ].copy()
fbsites.fb_id = fbsites.fb_id.str.strip('"')

fb_feed_url = 'https://graph.facebook.com/v2.10/{id}?fields=feed.fields(caption, id, created_time, link, name, description){token}'

def get_link(url):
    for _ in range(5):
        try:
            return requests.get(url)
        except Exception as err:
            print('Connection error: ', err)
            sleep(5)

def get_fbfeed(url):
    '''
    loads feeds as list of dict
    '''
    response = get_link(url).json()
        
    if not 'feed' in response:
        return None, None
    response = response['feed']
    if not 'data' in response:
        return None, None
    feed_df = pd.DataFrame(response['data'])
    feed_df.created_time = pd.to_datetime(feed_df.created_time)
        return feed_df, response.get('paging', {}).get('next', None)

aff_fb_feeds = []
for i, site in fbsites.iterrows():
    feed_url = fb_feed_url.format(id=site['fb_id'], token=token)
    feed_df, next_page = get_fbfeed(feed_url)
    if not isinstance(feed_df, pd.core.frame.DataFrame):
        continue
    while (pd.to_datetime('now') - min(feed_df.created_time)) < pd.Timedelta('1 day') and next_page != None:
        more_posts, next_page = get_fbfeed(next_page)
        feed_df = pd.concat([feed_df, more_posts])
    aff_fb_feeds.append(feed_df)
    sleep(3)

allposts = pd.concat(aff_fb_feeds)
allposts = allposts.reset_index(drop=True)
allposts.created_time = pd.to_datetime(allposts.created_time, utc=True).apply(
    lambda t: t.tz_convert('Europe/Kiev'))
allposts['unix_time'] = allposts.created_time.apply(lambda x: x.value // 10**9)
allposts.created_time = allposts.created_time.astype(str)
allposts['grid'] = None
allposts['postid'] = None
allposts.loc[:, ['grid', 'postid']] = allposts.id.str.split('_').values.tolist()
del(allposts['id'])
allposts = allposts.loc[pd.notnull(allposts.link), ]
allposts = allposts.loc[~allposts.link.str.contains('https://www.facebook.com|youtu.*be'), ]

allposts.link = allposts.link.apply(
    lambda l: get_link(l).url.replace('%', '%%')
    if 'bit.ly' in l or 'goo.gl' in l
    else l.replace('%', '%%'))

allposts.to_sql('fbfeeds', psql, index=False, if_exists='append')

endtime = pd.to_datetime('now', utc=True).tz_convert('Europe/Kiev')

print('{dt} loaded fb feeds in {timing}'.format(dt=endtime, timing=str(endtime-start)))