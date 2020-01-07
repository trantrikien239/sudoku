import scrapy

class WebSudoku(scrapy.Spider):
    name = 'websudoku'

    def start_requests(self):
        for level in range(2,5):
            for id in range(1000):
                yield scrapy.Request(
                    url=f'http://nine.websudoku.com/?select=0&level={level}&set_id={id}',
                    callback=self.parse
                )

    def parse(self, response):
        # result = response.xpath('//*[@id="cheat"]/@value').get()
        # display = response.xpath('//*[@id="editmask"]/@value').get()\
        #     .replace('0', '.').replace('1', '0').replace('.','1')
        yield {
            'level': response.xpath('//*[@name="level"]/@value').get(),
            'result': response.xpath('//*[@id="cheat"]/@value').get(),
            'display': response.xpath('//*[@id="editmask"]/@value').get()\
            .replace('0', '.').replace('1', '0').replace('.','1')
        }