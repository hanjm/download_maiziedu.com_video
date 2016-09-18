# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
from scrapy import Request


class DownloadMaizieduVideoPipeline(object):
    def process_item(self, item, spider):
        return item


class MyFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        print(self.files_urls_field)
        print(item.get("file_url"))
        yield Request(item.get(self.files_urls_field))

    def process_item(self, item, spider):
        return item
