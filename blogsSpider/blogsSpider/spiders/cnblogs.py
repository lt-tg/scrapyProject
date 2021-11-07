import scrapy
from undetected_chromedriver import v2 as uc
from scrapy import Request
from urllib import parse

class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['https://news.cnblogs.com/']
    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def start_requests(self):
        #入口模拟登录，获得cookie
        driver = uc.Chrome()
        driver.get("https://account.cnblogs.com/signin")
        input("回车继续：")
        cookies = driver.get_cookies()
        cookie_dic = {}
        for cookie in cookies:
            cookie_dic[cookie['name']] = cookie['value']
        for url in self.start_urls:
            headers = {
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
            }
            yield Request(url, cookies=cookie_dic, headers=headers, dont_filter=True)

    def parse(self, response):
        """
        1.提取本页面中的新闻url列表
        2.提取下一个页面的url
        3.提取新闻列表中带封面的新闻图片url
        """
        post_nodes = response.css("#news_list .news_block")
        for node in post_nodes:
            img_url = node.css(".entry_summary a img::attr(href)").extract_first("")
            post_url = node.css("h2 a::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": img_url}, callback=self.parse_detail)

        # next_url = response.css("div.pager a:last-child::attr(text)").extract_frist("")
        # if next_url == "Next >":
        #     next_url = response.css("div.pager a:last-child::attr(href)").extract_frist("")
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        next_url = response.xpath("//a[contains(text(), 'Next >']/@href").extract_first("")
        yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        pass

