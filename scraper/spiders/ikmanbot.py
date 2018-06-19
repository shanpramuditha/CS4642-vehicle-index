import scrapy
from urllib.parse import urljoin
import logging
import re

class IkmanBot(scrapy.Spider):
    name = "ikmanbot"
    # allowed_domains = ["https ://ikman.lk"]
    start_urls = []
    for i in range(300,500):
        start_urls.append("https://ikman.lk/en/ads/sri-lanka/cars-vehicles?page="+str(i))
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'vehicles.csv'
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
        breadcum = response.css("nav.ui-crumbs ol li a span::text").extract()
        values = response.css('div.item-properties dl dd::text').extract()
        print(properties)
        print(values)
        # exit(0)
        scraped_info = {
            'title': title,
            'price': price,
            'district' : breadcum[2],
            'town' : breadcum[3],
            'main category': breadcum[4],
            'sub category':breadcum[5]
        }
        for property in zip(properties,values):

            value = property[1].replace("cc","")
            value = value.replace("km","")

            scraped_info[property[0].replace(":","")] = value
        yield scraped_info