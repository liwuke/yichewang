import scrapy
import copy
from yichewang.items import YichewangItem
from time import sleep


class CarSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['car.yiche.com']
    start_urls = ['https://car.yiche.com']

    def parse(self, response):
        item = YichewangItem()
        alpha_list = response.css('div.brand-list>div')
        sort=1
        for alpha in alpha_list:
            item['sort']=sort
            letter = alpha.css('div.item-letter::text').extract_first()
            item['letter'] = letter
            brand_list = alpha.css('div.item-brand')
            sort+=1
            for brand in brand_list:
                brand_name = brand.css('a>div::text').extract_first()
                logo = brand.css('img::attr(data-original)').extract_first()
                item['brand_name'] = brand_name
                item['logo'] = 'https://' + logo
                id = brand.css('a>div::attr(data-id)').extract_first()
                item['type'] = False
                url = 'https://car.yiche.com/xuanchegongju/?mid=' + str(id)
                yield scrapy.http.Request(url, callback=self.pages, meta={'item': copy.deepcopy(item)},
                                          dont_filter=True)

    # def parse(self,response):
    #     url='https://car.yiche.com/xuanchegongju/?mid=77'
    #     self.item['type']=False
    #     self.item['id']=77
    #     self.item['letter']='A'
    #     self.item['brand_name']='奥迪'
    #     yield scrapy.http.Request(url,callback=self.pages,meta={'item':copy.deepcopy(self.item)},dont_filter=True)

    def pages(self, response):
        car_list = response.css('div.search-result-list>div')
        item = response.meta['item']
        count = 1
        for car in car_list:
            car_name = car.css('a>p::text').extract_first()
            data_id = car.css('::attr(data-id)').extract_first()
            item['data_id'] = data_id
            item['car_name'] = car_name
            item['type'] = True
            if count > 1:
                item['new_page'] = False
            else:
                item['new_page'] = True
            count += 1
            yield scrapy.Request(response.url, callback=self.car_type, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)
        if response.css('div#pagination-list>div.pagenation-box.ssr-box>a[class="link-btn next pg-item"]'):
            current_page = response.css(
                'div#pagination-list>div.pagenation-box.ssr-box>div>a.link-btn.active::text').extract_first()
            page_list = response.css('div#pagination-list>div.pagenation-box.ssr-box>div>a')
            for page in page_list:
                page_index = page.css('a::text').extract_first()
                if current_page == page_index:
                    new_url = response.url + '&page=' + str((int(page_index) + 1))
                    item['type'] = False
                    yield scrapy.Request(new_url, callback=self.pages, meta={'item': copy.deepcopy(item)},
                                         dont_filter=True)

    def car_type(self, response):
        response.meta['item']['type'] = False
        type_list = response.css('span.ck-cx-list-wrapper>div.ck-cx-list-content>a')
        item = response.meta['item']
        for type in type_list:
            type_name = type.css('div>div:nth-child(1)::text').extract_first() + \
                        ' / ' + \
                        (type.css('div>div:nth-child(2)::text').extract_first() if type.css(
                            'div>div:nth-child(2)::text') else '暂无数据') + \
                        ' / ' + \
                        type.css('div>div:nth-child(3)::text').extract_first() if type.css(
                'div>div:nth-child(3)::text') else '暂无数据'
            item['type_name'] = type_name
            yield item
