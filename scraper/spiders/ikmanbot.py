import scrapy
from urllib.parse import urljoin
import logging

class IkmanBot(scrapy.Spider):
    name = "ikmanbot"
    # allowed_domains = ["https://ikman.lk"]
    start_urls = []
    for i in range(1,30):
        start_urls.append("https://ikman.lk/en/ads/sri-lanka/cars-vehicles?page="+str(i))
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'test.csv'
    }
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )
    def parse(self, response):

        urls = response.css("a.item-title::attr(href)").extract()
        # urls = urls[:2]
        self.logger.info('urls %i', len(urls))
        for url in urls:
            url = urljoin("https://ikman.lk", url)
            self.logger.info('Parse function called on %s', url)
            yield scrapy.Request(url, callback=self.parse_vehicle)

    def parse_vehicle(self,response):
        title = response.css('div.item-top h1::text').extract()[0]
        price = response.css('span.amount::text').extract()[0]
        properties = response.css('div.item-properties dl dt::text').extract()
        values = response.css('div.item-properties dl dd::text').extract()
        print(properties)
        print(len(properties))
        scraped_info = {
            'title': title,
            'price': price
        }
        for property in zip(properties,values):
            scraped_info[property[0]] = property[1]
        yield scraped_info