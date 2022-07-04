import scrapy
from ..items import GswItem

class GsSpider(scrapy.Spider):
    name = 'gs'
    allowed_domains = ['gushiwen.org', 'gushiwen.cn']  # 修改，增加一个相似域名
    start_urls = ['https://www.gushiwen.cn/default_1.aspx']  # 修改为起始第一个URL地址，爬虫程序就是从这一页开始数据的

    # 该爬虫先从上面起始的第一个URL地址开始发出请求，并得到请求响应的数据，得到响应数据后，数据的解析就用如下的parse函数进行解析
    def parse(self, response):
        gsw_divs = response.xpath('//div[@class="left"]/div[@class="sons"]')  # xpath返回的是列表(每个div sons标签，也就是每首诗)
        for gsw_div in gsw_divs:  # 对每首诗进行遍历
            title = gsw_div.xpath('.//b/text()').extract_first()  # xpath返回的是列表(取列表第一个也就是诗的标题)
            if title:
                source = gsw_div.xpath('.//p[@class="source"]/a/text()').extract()  # 获取 作者 和 朝代 的列表
                author = source[0]   # 获取 作者
                dynasty = source[1]  # 获取 朝代
                content_lst = gsw_div.xpath('.//div[@class="contson"]//text()').extract()  # 获取 诗的文本内容
                content = ''.join(content_lst).strip()  # 列表中的每个元素用空串拼接，去除列表并用strip()方法移除字符串头尾指定的字符
                # 方式一
                # item = GswItem()  # 创建items对象并赋值
                # item['title'] = title
                # item['author'] = author
                # item['dynasty'] = dynasty
                # item['content'] = content
                # 方式二
                item = GswItem(title=title, author=author, dynasty=dynasty, content=content)  # 创建items对象并赋值
                yield item  # 将item数据传给管道 pipelines

        # 翻页逻辑处理
        next_href = response.xpath('//a[@id="amore"]/@href').get()
        if next_href:
            # next_url = 'https://www.gushiwen.cn' + next_href[0]  # URL第一种补全方式
            next_url = response.urljoin(next_href)  # URL第二种补全方式(urljoin可以进行URL地址的补全)
            yield scrapy.Request(next_url)  # 爬虫程序重新通过 爬虫引擎 调度器 下载器 请求下一页的数据
            # yield scrapy.Request(url=next_url, callback=self.parse)  # 或者这种方式请求






