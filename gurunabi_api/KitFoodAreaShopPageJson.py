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


def gnavi_api(count):
    latitude = '36.5310338';
    longitude = '136.6284361';
    key = 'Your API Key'
    url = "http://api.gnavi.co.jp/RestSearchAPI/20150630/"
    hit_per_page = '100'
    offset_page = str(count)
    search_range = '4'
    params = urllib.parse.urlencode({
        'format': 'json',
        'keyid': key,
        'latitude': latitude,
        'longitude': longitude,
        'hit_per_page': hit_per_page,
        'offset_page': offset_page,
        'range': search_range
    })
    #},encoding='utf-8')
    try:
        responce = urllib.request.urlopen(url + '?' + params)
        return responce.read()
    except:
        raise Exception(u'APIアクセスに失敗しました')


def do_json(data, check_count):
    parsed_data = json.loads(data)
    #print(data)

    if 'error' in parsed_data:
        if 'message' in parsed_data:
            raise Exception(u'{0}'.format(parsed_data['message']))
        else:
            raise Exception(u'データ取得に失敗しました')
    total_hit_count = int(parsed_data.get('total_hit_count', 0), 10)

    if total_hit_count < 1:
        raise Exception(u'指定した内容ではヒットしませんでした\nレストランデータが存在しなかったため終了します')
    print('{0}件ヒットしました。'.format(total_hit_count))
    print('---')

    #with open('kit_food_shop_address.json', 'a', encoding='utf-8') as f:
    with open('kit_food_shop_address.json', 'a', encoding='utf-8') as f:
        #f.write('{"kit_food_area":[')
        for (count, rest) in enumerate(parsed_data.get('rest')):
            f.write('{')
            access = rest.get('access', {})
            id_ = u'"id" : "{0}"'.format(rest.get('id', ''))
            name = u'"name" : "{0}"'.format(rest.get('name', ''))
            name_kana = u'"name_kana" : "{0}"'.format(rest.get('name_kana', ''))
            latitude = u'"latitude" : "{0}"'.format(rest.get('latitude', 0))
            longitude = u'"longitude" : "{0}"'.format(rest.get('longitude', 0))
            address = u'"address" : "{0}"'.format(rest.get('address', ''))
            opentime = u'"opentime" : "{0}"'.format(rest.get('opentime', ''))
            holiday = u'"holiday" : "{0}"'.format(rest.get('holiday', ''))
            tel = u'"tel" : "{0} "'.format(rest.get('tel', ''))
            access_line = u'"access_line" : "{0}"'.format(access.get('line', ''))
            access_station = u'"access_station" : "{0}"'.format(access.get('station', ''))
            access_walk = u'"access_walk" : "{0}分"'.format(access.get('walk', ''))
            budget = u'"budget" : "{0}"'.format(rest.get('budget', 0))
            #party = u'"party" : "{0}"'.format(rest.get('party',''))
            #lunch = u'"lunch" : "{0}"'.format(rest.get('lunch',''))
            categories= rest.get('code', {}).get('category_name_s', [])
            category_names = '"category_names" : {0}'.format(list(filter(lambda n: isinstance(n, (str)), categories)))
            single, double = '\'', '\"'
            category_names = category_names.replace(single,double)
            opentime = opentime.replace('\n','')
            holiday = holiday.replace('\n', '')
            result_list = [id_, name, name_kana, latitude, longitude, address, tel, opentime, holiday,  access_line, access_station, access_walk,  budget, category_names]
            result = '\t'.join(result_list)

            result_json = ','.join(result_list)
            f.write(result_json)

            if(total_hit_count/100 <= check_count and count == len(parsed_data['rest']) - 1):
                print(len(parsed_data['rest']))
                f.write('}')
            else:
                f.write('},')
            #f.close()
            print(result)

    print('---')
    print(u'{0}件出力しました'.format(count+1))
    return total_hit_count

if __name__ == '__main__':
    file_name = "kit_food_shop_address.json"
    if os.path.exists(file_name):
        os.remove(file_name)
    with open('kit_food_shop_address.json', 'a', encoding='utf-8') as f:
        f.write('{"kit_food_area":[')
    count = 1
    while(1):
        my = gnavi_api(count)
        totalCount = do_json(my, count)
        if(totalCount/100 <= count):
            with open('kit_food_shop_address.json', 'a', encoding='utf-8') as f:
                f.write(']}')
            print('finish')
            break
        else:
            print(totalCount)
            print(totalCount%100)
            print(count)
            count += 1
