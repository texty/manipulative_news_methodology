import codecs, feedparser, re, os, pickle
import pandas as pd
from sqlalchemy import create_engine
from time import sleep
from dateparser import parse as parsedate
from bs4 import BeautifulSoup

os.chdir('./propaganda/')

now = pd.to_datetime('now', utc=True).tz_convert('Europe/Kiev')

with open('psql_engine.txt', 'r') as f:
    engine = create_engine(f.read())

sites = pd.read_csv('sites_ids.csv')

replace_dates = [('нояб.*|листоп.*', 'November'),
                 ('дек.*|груд.', 'December'),
                 ('січ.*|янв.*', 'January'),
                 ('фев.*|лют.*', 'February'),
                 ('мар.*|берез.*', 'March'),
                 ('апр.*|квіт.*', 'April'),
                 ('ма[йя].*|трав.*', 'May'),
                 ('июн.*|черв.*', 'June'),
                 ('июл.*|лип.?н.*', 'July'),
                 ('авг.*|серп.?.*', 'August')]

now = pd.to_datetime('now', utc=True).tz_convert('Europe/Kiev')


def get_date(date):
    '''
    parses dates from strange
    '''
    if pd.isnull(date):
        return

    parsed = parsedate(date)

    if parsed:
        if parsed.year < 2017:
            return

        parsed = pd.to_datetime(parsed)
    else:
        for repl in replace_dates:
            date = re.sub(repl[0], repl[1], date)
        parsed = pd.to_datetime(parsedate(date))
        if not parsed:
            return now

    if parsed.tz:
        if now.tz_convert(parsed.tz) < parsed:
            parsed = parsed.tz_localize(None).tz_localize('Europe/Kiev')
    else:
        parsed = parsed.tz_localize('Europe/Kiev')

    parsed = parsed.tz_convert('Europe/Kiev')

    if parsed > (now - pd.DateOffset(days=1)) and parsed <= now:
        return parsed


feed_dfs = []
for i, site in sites.loc[pd.notnull(sites.rss),].iterrows():
    for i in range(5):
        feed = feedparser.parse(site['rss'])
        df = pd.DataFrame(feed.entries)
        if len(df.columns) > 0:
            break
        else:
            if i == 4:
                print('\tProblem while loading feed for {}'.format(site['rss']))
            if i < 4:
                sleep(5)
    if len(df.columns) < 1 or len(df) < 1:
        continue

    df['site'] = site['source']
    if not 'published' in df.columns:
        df['published'] = now
        df['published_parsed'] = now.tz_convert('UTC').value // 10 ** 9
    else:
        df.published = df.published.apply(get_date)
        df = df.loc[pd.notnull(df.published),]
        df.published_parsed = df.published.apply(lambda x: x.tz_convert('UTC').value // 10 ** 9)

    df['site'] = site['source']
    site_links = pd.read_sql("SELECT link FROM rss WHERE site = '{source}' AND published_parsed > {yesterday};".format(
        source=site['source'], yesterday=((now - pd.DateOffset(days=1)).value // 10**9)
                                         ), engine).link.tolist()
    df = df.reindex(columns=['site', 'link', 'published', 'published_parsed', 'title', 'summary', 'tags'])
    df = df.loc[~df.link.isin(site_links), ]
    if len(df) > 0:
        feed_dfs.append(df)

allfeeds = pd.concat(feed_dfs)

deltags = codecs.open('deltags.txt', 'r', encoding='utf-8').readlines()
deltags = list(map(lambda s: re.sub('[\-\s+]', ' ', s.strip().lower()), deltags))
deltags = '|'.join(deltags)

allfeeds = allfeeds.loc[~allfeeds.tags.astype('str').str.lower().str.contains(deltags), ]

allfeeds.loc[pd.notnull(allfeeds.tags), 'tags'] = allfeeds.loc[pd.notnull(allfeeds.tags), 'tags'].apply(
    lambda tags: '[{}]'.format(', '.join(list(map(lambda tag: tag.term ,tags)))))

def remove_html(html):
    '''
    Removes all html tags and specific symbols as &quot; from text
    '''
    return BeautifulSoup('<body>{}</body>'.format(html), 'html.parser').body.get_text(separator=' ')

allfeeds.title = allfeeds.title.apply(remove_html)
allfeeds.summary = allfeeds.summary.apply(remove_html)

allfeeds.published = allfeeds.published.apply(lambda t: t.tz_localize(None))

try:
    allfeeds.to_sql('rss', engine, index=False, if_exists='append')
except ValueError:
    with open('ValueErrorSQL.pkl', 'wb') as f:
        pickle.dump(allfeeds, f)
    print('{} Inadequate time zones, quiting\n'.format(now))
    quit()

timing = pd.to_datetime('now', utc=True).tz_convert('Europe/Kiev') - now

print(now, 'loaded feeds in {}\n'.format(str(timing)))