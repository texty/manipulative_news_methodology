import pandas as pd, pycld2 as cld2, re, langid
from sqlalchemy import create_engine
from bs4 import BeautifulSoup

from tqdm import tqdm

langid.set_languages(['ru','uk','en'])

with open('../psql_engine.txt') as f:
    psql = create_engine(f.read())

def get_lang(text):
    rel, _, matches = cld2.detect(text)
    if not rel:
        return
    matches = list(filter(lambda m: m[1] in ['ru', 'uk', 'en'], matches))
    if len(matches) == 0:
        return langid.classify(text)[0]
    return matches[0][1]
    
chunks = pd.read_sql('''SELECT html_id, ra_summary FROM htmls
                        WHERE lang isnull and ra_summary notnull; 
                     ''', psql, chunksize=20000)

for df in tqdm(chunks):
    df['text'] = df.ra_summary.apply(lambda s: re.sub('\s+', ' ', BeautifulSoup(s, 'lxml').get_text()).strip())
    df['text'] = df.text.apply(lambda t: ''.join([ch for ch in t if ch.isprintable()]))
    df['lang'] = df.text.apply(get_lang)
    vals = ',\n'.join([f"({html_id}, '{lang}')" for html_id, lang
                       in df.loc[pd.notnull(df.lang)].reindex(['html_id', 'lang'], axis=1).values])
    psql.execute(f'''
                 update htmls as t set
                     lang = c.lang
                 from (values
                     {vals}
                 ) as c(html_id, lang) 
                 where c.html_id = t.html_id;
                 ''')