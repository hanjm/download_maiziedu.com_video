# -*- coding: utf-8 -*-
# @Author: hanjinming
# @Date:   2016-08-02 08:53:49
# @Last Modified by:   hanjinming
# @Last Modified time: 2016-08-02 10:02:58

import os
import re
import sys
import multiprocessing
import urllib2
from Queue import Queue


# 课程标题
def parse_title(string):
    regexp = re.compile(r'<title>.+?</')  # match title
    title = regexp.findall(string)[0][7:][:-2]
    return title


# 课程视频小标题
def parse_items(string):
    regexp = re.compile(r'<span class="fl">[0-9]{1,2}.+?</span>')  # match item
    raw_items = regexp.findall(string)
    items = [raw_item[17:][:-7].decode('utf-8') + '.mp4'.decode('utf-8') for raw_item in raw_items]
    return items


# 第一个视频播放地址
def parse_href(string):
    regexp = re.compile(r'/course/[0-9]{3}-[0-9]{4}/')  # match video href
    href = regexp.findall(string)[0]
    return href


# 视频url元组
def parse_videos(string, count):
    regexp = re.compile(r'http://.+?-[0-9]{2}\.mp4')  # match video url
    url_base = regexp.findall(string)[0][:-7]
    count_list = list(range(1, count + 1))
    videos = [url_base + '-%02d.mp4' % i for i in count_list]
    return videos


def download_file(url, filename, overwrite=False):
    if not overwrite:
        if os.path.exists(filename):
            print 'file %s already existed, skip it' % filename
            return
    file_data = urllib2.urlopen(url).read()
    with open(filename, 'wb') as fp:
        fp.write(file_data)
    print 'file %s is saved!' % filename


if __name__ == '__main__':
    if not os.path.exists('url.txt'):
        print 'url.txt not found!'
        sys.exit(1)
    with open('url.txt') as fp:
        urls = fp.readlines()
    count = len(urls)  # 条目总数
    for index, url in enumerate(urls):
        print 'process %d of %d: %s' % (index + 1, count, url)
        print 'matching...'
        html = urllib2.urlopen(url[:34]).read()
        course_title = parse_title(html)
        print 'matched title:%s' % course_title
        if not os.path.exists(course_title.decode('utf-8')):
            os.mkdir(course_title.decode('utf-8'))
        os.chdir(course_title.decode('utf-8'))
        items = parse_items(html)
        print 'this course have %d items.' % len(items)
        video_href = 'http://www.maiziedu.com' + parse_href(html)
        video_html = urllib2.urlopen(video_href).read()
        videos = parse_videos(video_html, len(items))
        pool = multiprocessing.Pool(2)
        for i in range(len(items)):
            pool.apply_async(download_file, args=(videos[i], items[i]))
        pool.close()
        pool.join()
