# -*- coding: utf-8 -*-
import re
from gzip import GzipFile
from json import JSONDecoder
from sys import stdout
from urllib.parse import unquote
from urllib.request import build_opener

import pyecharts.options as opts
from pyecharts.charts import Line

user_cookies = input('Enter cookies: ')
user_id = re.search(r'_uid=(\d+)', user_cookies)
if not user_id:
    print('Invalid cookies')
    exit(0)

user_id = user_id[1]

opener = build_opener()
opener.addheaders = [
    ('Accept', 'text/html,application/xhtml+xml,application/xml;\
        q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'),
    ('Accept-Charset', 'utf-8'),
    ('Accept-Language', 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'),
    ('Accept-Encoding', 'gzip, deflate, br'),
    ('Cookie', user_cookies),
    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'),
    ('sec-ch-ua', '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"')
]

def decompress_response(response):
    cs = response.getheader('Content-Type')
    cs = cs[cs.rfind('=') + 1:]
    if response.getheader('Content-Encoding') == 'gzip':
        with GzipFile(fileobj=response) as gz:
            return gz.read().decode(cs)
    return response.read().decode(cs)

json_pattern = re.compile(r'decodeURIComponent\("(.*?)"\)')
def get_luogu_json(url):
    with opener.open(url, timeout=5) as response:
        html = decompress_response(response)
        json_str = unquote(json_pattern.search(html)[1])
        return JSONDecoder().decode(json_str)['currentData']

user_data = get_luogu_json(f'https://www.luogu.com.cn/user/{user_id}')['user']
print('-', end='')
stdout.flush()
username = user_data['name']
elo_data = user_data['elo']
X = []
Y = []
count = 1
while elo_data:
    contest_id = elo_data['contest']['id']
    elo_data = get_luogu_json(f'https://www.luogu.com.cn/contest/{contest_id}')['userElo']
    X.append(elo_data['contest']['name'])
    Y.append(elo_data['rating'])
    print('-', end='')
    stdout.flush()
    elo_data = elo_data['previous']
print()

X.reverse()
Y.reverse()

title = f'{username} 的洛谷 Rating'

chart = (
    Line(
        init_opts=opts.InitOpts(
            width='1000px',
            height='600px',
            page_title=title
        )
    )
    .add_xaxis(X)
    .add_yaxis('rating', Y)
    .set_global_opts(
        title_opts=opts.TitleOpts(title=title, subtitle='Made with LuoguRatingGraph')
    )
)

chart.render('rating.html')
print('图表已保存至 rating.html。')