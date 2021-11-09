import scrapy
import time
import numpy as np

class WebSudoku(scrapy.Spider):
    name = 'websudoku'
    download_delay = 5.1932

    def start_requests(self):
        for level in range(1,5):
            for id in range(1000):
                yield scrapy.Request(
                    url=f'http://nine.websudoku.com/?select=0&level={level}&set_id={id}',
                    callback=self.parse
                )
                
                time.sleep(np.random.rand() + 0.5)

    def parse(self, response):
        yield {
            'level': response.xpath('//*[@name="level"]/@value').get(),
            'result': response.xpath('//*[@id="cheat"]/@value').get(),
            'display': response.xpath('//*[@id="editmask"]/@value').get()\
            .replace('0', '.').replace('1', '0').replace('.','1')
        }