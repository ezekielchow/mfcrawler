import scrapy
import logging
from itertools import islice


class PublicMutualSpider(scrapy.Spider):
    name = "public_mutual"

    def start_requests(self):
        urls = [
            'https://www.publicmutual.com.my/Home/UT-Fund-Prices',
        ]
        for url in urls:
            formdata = '__VIEWSTATEGENERATOR=CA0B0334&__EVENTVALIDATION=2GhFBaqQac8%2B0zJAFmrTxSrMs8Mr6JeK%2BxNTzX24QmeBLGd7KQSXv3%2BCZRA%2F6CzlWA9f1%2FWlyjkuHXqda7Nuk4K2rePo4j4ZjknuB26MCZRgby5fYwT7M%2BBKix9YmNhpVatw2UFl%2BJT%2FLH4hBUFFTpT7KNo7Ff9htutJYUTXLjOV5eMkrT6UpVxSKmLxUyujpTDtOHvBeWCJ0bmjWoTC1%2FVRxlJAtVI%2BENS9Olqq9jJ8UPKXGomTFdrF%2B%2BOYaT5OSKC8ZbWpr5dwpSYmwGcIMX3WkJfEVarf99s%2B5HzK%2BGRnnmH70Hrxp6PkyqHWfGcGS%2F5auonIqCfGeWDAqYYGpb%2BvlkuTsSOlg2gI1N0a2hsefluS&dnn%24ctr911%24FPFundPrice%24ddlSeries=All&dnn%24ctr911%24FPFundPrice%24ddlFund=All&__RequestVerificationToken=yeEnW5wbxMX0k58TKVfvmMZd811D5BzYcv8fORxrwITyB5yVJ-HCmvaCkHqpqkpPh6MF5g2&__ASYNCPOST=true&__VIEWSTATE=WIR7Pv3RnR6%2Bz0DY7ywNuOlJtPmDY4kBuV5Xs15hJcGEGfKV%2Fk2WvpQyRXuO%2BbCDl1noSA%3D%3D'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            request = scrapy.Request(
                url=url, callback=self.parse, method='POST', headers=headers)
            request = request.replace(body=formdata)
            yield request

    def parse(self, response):
        rows = response.selector.xpath('//table[@class="fundtable"]/tr')
        rowsiters = iter(rows)
        next(rowsiters)
        for row in islice(rows, 1, None):
            yield {
                'date': row.xpath('td[1]/text()').extract(),
                'fund': row.xpath('td[2]/text()').extract(),
                'fund_abbr': row.xpath('td[3]/text()').extract(),
                'nav': row.xpath('td[4]/text()').extract(),
            }
