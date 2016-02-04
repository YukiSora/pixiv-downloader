# -*- coding: utf8 -*-
import json
import sys

from webIO import *

history = {}

def rankDownloader(mode = 'daily', content = 'illust', date = '', n = 150):
    global history
    with open('history.json', 'r') as f:
        history = json.loads(f.read())

    workList = []
    for p in range(1, int((n - 1) / 50) + 2):
        data = {
            'mode' : mode,
            'content': content,
            'date' : date,
            'p' : p
        }
        workList += _getWorkList(data)

    with open('history.json', 'w') as f:
        f.write(str(history))

    return _download(workList[:n])

def _getWorkList(data):
    rank = getRank(data)

    if rank['status'] != "success":
        print('[error] Load rank filed.')
        sys.exit(1)

    workList = []
    for work in rank['response'][0]['works']:
        data = _analysis(work)
        if data:
            workList.append(data)

    return workList

def _analysis(work):
    if not str(work['work']['id']) in history:
        history[str(work['work']['id'])] = True

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
    else :
        return None

def _download(workList):
    count = 0
    for work in workList:
        for i in range(work['work']['count']):
            data = {
                'url' : work['work']['url'].replace('p0', 'p' + str(i)),
                'path' : 'image/' + str(work['work']['id']) + '_p' + str(i) + '.' + work['work']['url'][-3:],
                'str' : str(work['rank']) + '. ' + str(work['work']['id']) + '_p' + str(i) + '.' + work['work']['url'][-3:]
            }
            downloadImage(data)
            count += 1

    return count
