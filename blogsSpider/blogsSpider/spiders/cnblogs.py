import scrapy
from undetected_chromedriver import v2 as uc

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
            yield scrapy.Request(url, cookies=cookie_dic, headers=headers, dont_filter=True)

    def parse(self, response):
        url_list = response.xpath("//div[@id='news_list']//h2[@class='news_entry']/a/@href").extract()
        url_list = response.css('div#news_list h2 a::attr(href)').extract()
        print(url_list)
        pass
