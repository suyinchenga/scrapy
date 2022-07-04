# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class GswPipeline:

    def open_spider(self, spider):
        self.fp = open('gsw.txt', 'w', encoding='utf-8')

    # item 是从爬虫文件传递过来的数据，是GswItem类的一个实例化对象
    def process_item(self, item, spider):
        item_json = json.dumps(dict(item), ensure_ascii=False)
        self.fp.write(item_json + '\n')
        return item

    def close_spider(self, spider):
        self.fp.close()