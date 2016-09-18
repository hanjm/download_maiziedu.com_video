# coding=utf-8

import scrapy
import re

from download_maiziedu_video.items import FileItem


# generate video url and tile
class CourseVideoSpider(scrapy.Spider):
    name = 'video'
    regexp_url = re.compile('lessonUrl = "http://.+?mp4')

    def __init__(self, url=None, **kwargs):
        super(CourseVideoSpider, self).__init__(name=None, **kwargs)
        print(url)
        self.start_urls = [url]

    def parse(self, response):
        for i in response.xpath('//ul[@class="lesson-lists"]/li'):
            url = i.xpath('a/@href').extract_first()
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse_2rd)

    def parse_2rd(self, response):
        title = response.xpath('//li[@class="liH"]/a/span/text()').extract_first()
        title += '.mp4'
        url = response.selector.re(self.regexp_url)
        url = url[0].split('"')[1]
        yield {
            'title': title,
            'url': url,
        }


# directly fetch file via file pipelines
class CourseVideoFileSpider(scrapy.Spider):
    name = 'video_download'
    start_urls = ['http://www.maiziedu.com/course/395/']
    regexp_url = re.compile('lessonUrl = "http://.+?mp4')

    def parse(self, response):
        for i in response.xpath('//ul[@class="lesson-lists"]/li'):
            url = i.xpath('a/@href').extract_first()
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse_2nd)

    def parse_2nd(self, response):
        file_item = FileItem()
        file_item['file_name'] = response.xpath('//li[@class="liH"]/a/span/text()').extract_first() + '.mp4'
        file_item['file_url'] = response.selector.re(self.regexp_url)[0].split('"')[1]
        yield file_item


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute(['scrapy', 'crawl', 'video_download'])
