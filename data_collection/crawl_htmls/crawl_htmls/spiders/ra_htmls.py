import scrapy, re, pdb, pandas as pd, requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from crawl_htmls.items import RaResult
from urllib.parse import urlparse

with open('psql_engine.txt') as f:
    psql = create_engine(f.read())

unix_offset = (pd.to_datetime('now') - pd.DateOffset(days=30)).replace(hour=0, minute=0, second=0).value // 10**9

q = f'''
SELECT * FROM
(SELECT fbfeeds.link, fbfeeds.fbfeeds_id FROM fbfeeds
LEFT JOIN htmls ON (fbfeeds.link = htmls.link)
WHERE htmls.link ISNULL AND fbfeeds.unix_time > {unix_offset}
) AS fb
FULL OUTER JOIN
(SELECT rss.link, rss.rss_id FROM rss
LEFT JOIN htmls ON (rss.link = htmls.link)
WHERE htmls.link ISNULL AND rss.published_parsed > {unix_offset}
) AS r
ON (r.link = fb.link);
'''
raw = pd.read_sql(q, psql)

raw.columns = ['link', 'fbfeeds_id', 'link1', 'rss_id']
raw.link = raw.link.fillna(raw.link1)
del(raw['link1'])
raw = raw.sample(frac=1)

# raw = pd.read_sql(f'''
#                    select distinct link, fbfeeds_id, rss_id from htmls
#                    where (link ~~ '%%hromadske.ua%%' and is_other isnull)
#                       or link ~~ '%%alternatio.org%%';
#                    ''', psql)


class SitesCrawler(scrapy.Spider):
    name = 'ra_htmls'
    psql = psql
    
    custom_settings = {
        'CONCURRENT_ITEMS': 300,
        'URLLENGTH_LIMIT': 10000,
    }
    
    def start_requests(self):
        urls = raw.sample(frac=1).values
        
        blocked = ['tvzvezda.ru', 'tk-union.tv', 'novorossiatv.com', 'ria.ru',
                   'sputniknews.com', 'rian.com.ua', 'news-front.info',
                   'armiyadnr.su', 'lug-info.com', 'dnr-live.ru', 'dnr-pravda.ru',
                   'republic-tv.ru', 'dan-news.info']
        
        for link, fbfeeds_id, rss_id in urls:
            domain = urlparse(link).netloc
            if domain == 'hromadske.ua':
                link = link.replace('hromadske.ua', 'ru.hromadske.ua')
            if domain in blocked:
                yield scrapy.Request(link, callback=self.parse,
                                     meta={'link':link, 'fbfeeds_id': fbfeeds_id, 'rss_id': rss_id, 'proxy': 'http://localhost:8123',})
            else:
                yield scrapy.Request(link, callback=self.parse,
                                     meta={'link':link, 'fbfeeds_id': fbfeeds_id, 'rss_id': rss_id,})
    
    def parse(self, r):
        
        link = r.meta['link']
        domain = urlparse(link).netloc
        page_links = filter(lambda a: 'http' in a,
                            r.xpath('//a/@href').extract())
        page_links = map(lambda a: urlparse(a).netloc.replace('www.', ' '), page_links)
        page_links = list(set(filter(lambda a: a != domain, page_links)))
        if 'alternatio.org' in link or 'hromadske.ua' in link:
            soup = BeautifulSoup(r.body.decode('utf8', 'ignore'), 'lxml')
        else:
            soup = BeautifulSoup(r.body, 'lxml')
        [t.extract() for t in soup.find_all()
         if len(t.text.strip()) == 0
         or t.name in ['img', 'iframe', 'script', 'link', 'footer', 'meta']
         or re.search('nav|p[io]dval|footer|copyright|re[ck]lam', str(list(t.attrs.values())))
        ]
        try:
            d = requests.post('http://localhost:3000',
                              data={'raw_html': str(soup)}
                             ).json()
            assert len(d['title']) > 0
        except Exception as err:
            self.logger.info(f'Failed {r.url}')
            pass
        
        item = RaResult()
        item['link'] = r.meta['link']
        item['real_url'] = r.url
        item['ra_title'] = d['title']
        item['ra_summary'] = re.sub('\s+', ' ', d['content'])
        item['rss_id'] = r.meta['rss_id'] if pd.notnull(r.meta['rss_id']) else 'null'
        item['fbfeeds_id'] = r.meta['fbfeeds_id'] if pd.notnull(r.meta['fbfeeds_id']) else 'null'
        item['page_links'] = page_links
        
        yield item