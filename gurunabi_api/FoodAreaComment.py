#Python3 用のぐるなびAPIプログラム
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import urllib
import urllib.parse
import urllib.request
import requests
import json


def gnavi_api():
    #latitude = '36.5310338'
    #longitude = '136.6284361'
    key = 'Your API Key'
    url = "https://api.gnavi.co.jp/PhotoSearchAPI/20150630/"
    #hit_per_page = '100'
    #search_range = '4'
    latitude = '36.5310338';
    longitude = '136.6284361';
    search_range = '4'
    params = urllib.parse.urlencode({
        'format': 'json',
        'keyid': key,
        'latitude': latitude,
        'longitude': longitude,
        'range': search_range
    })
    """encoding = 'utf-8'
    menu_name = 'ハンバーグ'
    params = urllib.parse.urlencode({
        'format': 'json',
        'keyid': key,
        'menu_name': menu_name.encode(encoding)
    })"""
    #},encoding='utf-8')
    try:
        responce = urllib.request.urlopen(url + '?' + params)
        return responce.read()
    except:
        raise Exception(u'APIアクセスに失敗しました')


def do_json(data):
    parsed_data = json.loads(data)
    print(parsed_data)

    if 'error' in parsed_data:
        if 'message' in parsed_data:
            raise Exception(u'{0}'.format(parsed_data['message']))
        else:
            raise Exception(u'データ取得に失敗しました')
    # ヒット件数取得
    """total_hit_count = None
    if "total_hit_count" in parsed_data["response"] :
        total_hit_count = parsed_data["response"]["total_hit_count"]
    print('{0}件ヒットしました。'.format(total_hit_count))"""

    # レストラン検索APIの出力初期ディレクトリが異なるため
    response = parsed_data.get('response')
    total_hit_count = response.get('total_hit_count', 0)
    #total_hit_count = int(parsed_data.get('total_hit_count', 0), 10)
    if total_hit_count < 1:
        raise Exception(u'指定した内容ではヒットしませんでした\nレストランデータが存在しなかったため終了します')
    hit_per_page = response.get('hit_per_page')
    print(hit_per_page)
    print('{0}件ヒットしました。'.format(total_hit_count))
    print('---')

    for page in range(hit_per_page):
        page_dir = response.get(str(page))
        photo = page_dir.get('photo')
        comment = u'{0}'.format(photo.get('comment', ''))
        total_score = u'{0}'.format(photo.get('total_score', ''))
        result_list = [comment, total_score]
        result = '\t'.join(result_list)
        print(result)
    print('---')
    print(u'{0}件出力しました'.format(hit_per_page+1))


if __name__ == '__main__':
    my = gnavi_api()
    do_json(my)
