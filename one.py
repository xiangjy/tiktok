# -*- coding:utf-8 -*-

import re
import requests
from lxml import etree


def handle_decode(input_data, url):
    search_douyin_str = re.compile(r'抖音ID：')
    # 匹配icon font
    regex_list = [
        {'name':[' &#xe603; ',' &#xe60d; ',' &#xe616; '],'value':0},
        {'name':[' &#xe602; ',' &#xe60e; ',' &#xe618; '],'value':1},
        {'name':[' &#xe605; ',' &#xe610; ',' &#xe617; '],'value':2},
        {'name':[' &#xe604; ',' &#xe611; ',' &#xe61a; '],'value':3},
        {'name':[' &#xe606; ',' &#xe60c; ',' &#xe619; '],'value':4},
        {'name':[' &#xe607; ',' &#xe60f; ',' &#xe61b; '],'value':5},
        {'name':[' &#xe608; ',' &#xe612; ',' &#xe61f; '],'value':6},
        {'name':[' &#xe60a; ',' &#xe613; ',' &#xe61c; '],'value':7},
        {'name':[' &#xe60b; ',' &#xe614; ',' &#xe61d; '],'value':8},
        {'name':[' &#xe609; ',' &#xe615; ',' &#xe61e; '],'value':9},
    ]

    for i1 in regex_list:
        for i2 in i1['name']:
            input_data = re.sub(i2,str(i1['value']),input_data)

    html = etree.HTML(input_data)
    douyin_info = {}
    douyin_info['nick_name'] = html.xpath("//p[@class='user-info-name']/text()")[0]
    douyin_id = ''.join(html.xpath("//p[@class='user-info-id']/i/text()"))
    douyin_info['douyin_id'] = re.sub(search_douyin_str,'',html.xpath("//p[@class='user-info-name']/text()")[0]).strip() + douyin_id

    douyin_info['describe'] = html.xpath("//div[@class='user-title']/text()")[0].replace('\n',',')

    like = ''.join(html.xpath("//div[@data-item='like']/p[@class='count']//i[@class='icon iconfont ']/text()"))
    unit = html.xpath("//div[@data-item='like']/p[@class='count']/text()")
    if unit[-1].strip() == 'w':
        douyin_info['like'] = str(float(like)/10)+'w'
    else:
        douyin_info['like'] = like

    comment = ''.join(html.xpath("//div[@data-item='comment']//i[@class='icon iconfont ']/text()"))
    unit = html.xpath("//div[@data-item='comment']/p[@class='count']/text()")
    if unit[-1].strip() == 'w':
        douyin_info['comment'] = str((float(comment)/10))+'w'
    else:
        douyin_info['comment'] = comment

    return douyin_info


def handle_douyin_info(url):
    header = {
        'User-Agent':'Mozilla/5.0 (Linux;U;Android 2.3;en-us;Nexus One Build/FRF91)AppleWebKit/999+(KHTML, like Gecko)Version/4.0 Mobile Safari/999.9'
    }
    response = requests.get(url=url, headers=header)
    return handle_decode(response.text, url)

if __name__ == '__main__':
    url = 'https://www.iesdouyin.com/share/video/6681141729246186760/?mid=6659642087115328259'
    print handle_douyin_info(url)

