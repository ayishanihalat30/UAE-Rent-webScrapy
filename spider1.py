import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.request import urlopen


# subregion links extractor class

class SubregionLinksExtractor(scrapy.Spider):
    # scraper name
    name = 'bayut'

    # base URLs
    base_urls = ['https://www.bayut.com/to-rent/property/dubai/']

    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36'
    }

    # crawlre's entry point
    def start_requests(self):
        # loop over base URLs
        for url in self.base_urls:
            # init filename
            filename = url.split('/property')[0].split('-')[-1] + '.txt'

            # reset output file
            with open("filename.json", 'w') as f:
                f.write('')

            # make initial HTTP GET request
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                meta={
                    'filename': filename
                },
                callback=self.parse_region
            )
            # break

    # parse region callback method

    def parse_region(self, response):
        # get region links
        region_links = response.css('div[class="aeb96d72"]').css(
            'a::attr(href)').getall()

        # loop over the region links
        for region_url in region_links:
            # crawl next region
            yield response.follow(
                url=region_url,
                headers=self.headers,
                meta={
                    'filename': response.meta.get('filename')
                },
                callback=self.parse_subregions
            )
            break

    # parse subregions callback method
    def parse_subregions(self, response):
        # extract filename
        filename = response.meta.get('filename')

        # get subregion links
        subregion_links = [
            'https://www.bayut.com/' + link
            for link in
            response.css('div[class="aeb96d72"]').css('a::attr(href)').getall()
        ]

        # store subregion links to the text file
        with open("filename.txt", 'a') as f:
            f.write('\n' + '\n'.join(subregion_links))


# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(SubregionLinksExtractor)
    process.start()
