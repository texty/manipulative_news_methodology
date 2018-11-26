# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine
import pdb


class RaItemPipeline(object):

    def process_item(self, item, spider):
        q = f'''INSERT INTO htmls(link, real_url, ra_title, ra_summary, rss_id, fbfeeds_id, loaded_unix)
                VALUES ('{item['link'].replace("'", "''").replace('%', '%%')}',
                        '{item['real_url'].replace("'", "''").replace('%', '%%')}',
                        '{item['ra_title'].replace("'", "''").replace('%', '%%')}',
                        '{item['ra_summary'].replace("'", "''").replace('%', '%%')}',
                        {item['rss_id']},
                        {item['fbfeeds_id']},
                        extract(epoch from current_timestamp)::int
                        );
             '''
#         q = f'''update htmls set
#                         real_url = '{item['real_url'].replace("'", "''").replace('%', '%%')}',
#                         ra_title = '{item['ra_title'].replace("'", "''").replace('%', '%%')}',
#                         ra_summary = '{item['ra_summary'].replace("'", "''").replace('%', '%%')}',
#                         rss_id = {item['rss_id']},
#                         fbfeeds_id = {item['fbfeeds_id']},
#                         loaded_unix = extract(epoch from current_timestamp)::int
                        
#                     where link = '{item['link'].replace("'", "''").replace('%', '%%').replace('ru.hromadske.ua', 'hromadske.ua')}';
#              '''
        spider.psql.execute(q)
        spider.psql.execute(f'''insert into plinks values (
                               '{item['link'].replace("'", "''").replace('%', '%%')}',
                               ARRAY{item['page_links']}::text[]
                               )
                               on conflict (link) do nothing;
                           ''')
        spider.logger.info(f"wrote {item['link']}")
        return item
