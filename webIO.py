# -*- coding: utf8 -*-
import getpass
import requests
import sys

_session = None
_headers = {}

def initialization():
    global _session
    _session = requests.Session()

    global _headers
    _headers = {
        'Referer': 'http://www.pixiv.net/',
        'User-Agent': 'PixivIOSApp/5.7.2',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    return

def login():
    url = 'https://oauth.secure.pixiv.net/auth/token'

    postdata = {
        'username': input('Pixiv ID: '),
        'password': getpass.getpass('Password: '),
        'grant_type': 'password',
        'client_id': 'bYGKuGVw91e0NMfPGp44euvGt59s',
        'client_secret': 'HP3RmkgAmEGro0gn1x9ioawQE8WMfvLXDz3ZqxpK',
    }
    r = _request(method = 'POST', url = url, postdata = postdata)

    _headers.update({
        'Authorization': 'Bearer ' + r.json()['response']['access_token'],
        'Cookie': 'PHPSESSID=' + r.cookies['PHPSESSID']
    })

    return

def getRank(data):
    url = 'https://public-api.secure.pixiv.net/v1/ranking/all'
    params = {
        'mode': data['mode'],
        'page': data['p'],
        'date' : data['date'],
        'per_page': 50,
        'include_stats': False,
        'include_sanity_level': False,
        'image_sizes': 'large',
        'profile_image_sizes': 'px_50x50'
    }
    r = _request(method = 'GET', url = url, params = params)

    return r.json()

def downloadImage(data):
    with open(data['path'], 'wb') as f:
        r = _request(method = 'GET', url = data['url'], stream = True)

        currentLength = 0
        totalLength = int(r.headers.get('content-length'))

        print('\033[?25l', end = '')
        for chunk in r.iter_content(chunk_size = int(totalLength / 20)):
            f.write(chunk)
            currentLength += len(chunk)
            _processingBar(int(20 * currentLength / totalLength), data['str'])
        print('\033[?25h', end = '')

        if r.status_code == requests.codes.ok:
            print('\033[32mdone\033[0m')
        else:
            print('\033[31mfail\033[0m')

    return

def _processingBar(process, message):
    sys.stdout.write('\r%s: %3s%% %s%s ' % (message, str(process * 5), '\033[47m' + ' ' * process + '\033[0m', ' ' * (20 - process)))
    sys.stdout.flush()

    return

def _request(method, url, postdata = None, params = None, stream = False):
    if method == 'GET':
        return _session.get(url, headers = _headers, params = params, stream = stream, timeout = 10)
    else:
        return _session.post(url, headers = _headers, params = params, data = postdata, timeout = 10)
