import scrapy
import time
import numpy as np
import itertools

class WebSudoku(scrapy.Spider):
    name = 'websudoku'
    # download_delay = 5.1932

    def start_requests(self):
        size = 10000
        level_list = [np.random.randint(1,5) for i in range(size)]
        id_list = [np.random.randint(10000,20000) for i in range(size)]
        for level, id in zip(level_list, id_list):
            yield scrapy.Request(
                url=f'http://nine.websudoku.com/?select=0&level={level}&set_id={id}',
                callback=self.parse
            )
                

    def parse(self, response):
        yield {
            'level': response.xpath('//*[@name="level"]/@value').get(),
            'id': response.xpath('//*[@id="pid"]/@value').get(),
            'result': response.xpath('//*[@id="cheat"]/@value').get(),
            'display': response.xpath('//*[@id="editmask"]/@value').get()\
            .replace('0', '.').replace('1', '0').replace('.','1')
        }