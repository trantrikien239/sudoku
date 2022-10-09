import scrapy
import random
import time

class WebSudoku(scrapy.Spider):
    name = 'websudoku'

    def start_requests(self):
        # for level in range(1,5):
        for _ in range(4000):
            level = random.randint(1,4)
            id = random.randint(1,10_000)
            yield scrapy.Request(
                url=f'http://nine.websudoku.com/?select=0&level={level}&set_id={id}',
                callback=self.parse
            )

    def parse(self, response):
        yield {
            'level': response.xpath('//*[@name="level"]/@value').get(),
            'id': response.xpath('//*[@name="id"]/@value').get(),
            'result': response.xpath('//*[@id="cheat"]/@value').get(),
            'display': response.xpath('//*[@id="editmask"]/@value').get()\
            .replace('0', '.').replace('1', '0').replace('.','1')
        }