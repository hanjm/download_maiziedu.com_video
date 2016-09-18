# coding=utf-8
from exceptions import SystemExit
import json
import multiprocessing
import os
import urllib2
import sys

from scrapy.cmdline import execute


def download_file(url, filename, overwrite=False):
    if not overwrite:
        if os.path.exists(filename):
            print(u'file %s already existed, skip it' % filename)
            return
    file_data = urllib2.urlopen(url).read()
    with open(filename, 'wb') as fp:
        fp.write(file_data)
    print(u'file %s is saved!' % filename)


def parse_course(url):
    if os.path.exists('video_url.json'):
        os.remove('video_url.json')
    try:
        execute([
            'scrapy', 'crawl', 'video', '-o', 'video_url.json', '-a', 'url={}'.format(url)
        ])
    except SystemExit:
        print(u'Crawled course video urls.')
        pass
    with open('video_url.json') as fp:
        rv = json.loads(fp.read())
    rv.sort()
    count = len(rv)
    print(u'Start downloading... total %d items' % count)
    # processes = 2
    pool = multiprocessing.Pool(2)
    for i in range(count):
        pool.apply_async(download_file, args=(rv[i].get('url'), rv[i].get('title')))
    pool.close()
    pool.join()


if __name__ == '__main__':
    if not os.path.exists('url.txt'):
        print 'url.txt not found!'
        sys.exit(1)
    with open('url.txt') as fp:
        urls = fp.readlines()
    count = len(urls)  # 条目总数
    print(u'Start parsing... total %d items' % count)
    for index, url in enumerate(urls):
        course_dir = u'course{}'.format(index + 1)
        os.mkdir(course_dir)
        os.chdir(course_dir)
        parse_course(url)
        os.chdir('../')
