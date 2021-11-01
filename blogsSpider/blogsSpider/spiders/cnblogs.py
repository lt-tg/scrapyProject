import scrapy


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        url_list = response.xpath("//div[@id='news_list']//h2[@class='news_entry']/a/@href").extract()
        pass
