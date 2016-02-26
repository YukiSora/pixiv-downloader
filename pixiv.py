# -*- coding: utf8 -*-
import os

from downloader import *

def main():
    print('Welcome to use this Pixiv downloader.')
    initialization()
    login()
    if not os.path.exists('image'):
        os.makedirs('image')

    while True:
        print('Which daily do you want to download?')
        print('1. daily')
        print('2. daily_r18')
        mode = ['daily', 'daily_r18'][int(input()) - 1]
        print('Which date do you want to download? (Format: yyyy-mm-dd)')
        date = input()
        print('How many images do you want to download? (daily maximum 500, daily_r18 maximum 300)')
        n = int(input())

        if not os.path.exists('image/' + date):
            os.makedirs('image/' + date)

        print('Start downloading...')
        count = rankDownloader(mode = mode, date = date, n = n)
        print('%d images has been downloaded.' % (count))

    return

if __name__ == '__main__':
    main()
