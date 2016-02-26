# -*- coding: utf8 -*-
import json
import sqlite3
import sys

from webIO import *

def rankDownloader(mode = 'daily', content = 'illust', date = '', n = 50):
    workList = []
    for p in range(1, int((n - 1) / 50) + 2):
        data = {
            'mode' : mode,
            'content': content,
            'date' : date,
            'p' : p
        }
        rank = getRank(data)
        for work in rank['response'][0]['works']:
            workList.append(_analysis(work))

    return _download(workList[:n], 'image/' + date + '/')

def _analysis(work):
        return {
            'rank' : work['rank'],
            'work' : {
                'id' : work['work']['id'],
                'title' : work['work']['title'],
                'url' : work['work']['image_urls']['large'],
                'count' : work['work']['page_count']
            },
            'user' : {
                'id' : work['work']['user']['id'],
                'name' : work['work']['user']['name']
            }
        }

def _download(workList, path):
    conn = sqlite3.connect('pixiv.db')
    c = conn.cursor()

    count = 0
    for work in workList:
        c.execute("SELECT * FROM Record WHERE Work_ID = '%s'" % work['work']['id'])
        if not c.fetchone():
            for i in range(work['work']['count']):
                data = {
                    'url' : work['work']['url'].replace('p0', 'p' + str(i)),
                    'path' : path + str(work['work']['id']) + '_p' + str(i) + '.' + work['work']['url'][-3:],
                    'str' : str(work['rank']) + '. ' + str(work['work']['id']) + '_p' + str(i) + '.' + work['work']['url'][-3:]
                }
                downloadImage(data)
                count += 1
            c.execute("INSERT INTO Record VALUES ('%s', '%s')" % (work['work']['id'], work['user']['id']))

    conn.commit()
    conn.close()

    return count
