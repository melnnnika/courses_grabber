import scrapy

class MitSpider(scrapy.Spider):
    name = 'mit'
    custom_settings = {
        'ITEM_PIPELINES': {
            'courses_grabber.pipelines.Courses_grabberPipeline': 400
        }
    }
    start_urls = ['https://ocw.mit.edu/courses/']

    def parse(self, response):
        for href in response.xpath('//table[contains(@class, "courseList")]/tbody/tr/td[2]/a/@href').extract():
            yield scrapy.Request(response.urljoin(href),
                                callback=self.parse_course)


    def parse_course(self, response):
        instructors = {}
        category = response.xpath('//nav[contains(@id, "breadcrumb_chp")]//a[3]/text()').extract()
        if not category:
            category = response.xpath('//nav[contains(@id, "breadcrumb_chp")]//a[2]/text()').extract()
        for lector in response.xpath('//p[contains(@class, "ins")]/text()').extract():
            instructors[lector] = None
        yield {
            'name': response.xpath('//h1[contains(@class, "title")]/text()').extract()[0],
            'source': 'mit',
            'provider': 'mit',
            'category': category[0],
            'language': 'English',
            'duration': None,
            'duration_filter': None,
            'instructors_list': instructors,
            'start_date': response.xpath('//p[contains(@itemprop, "startDate")]/text()').extract(),
            'description': response.xpath('//div[contains(@itemprop, "description")]//p/text()').extract()[0],
            'link': response.url,
            'video': None,
            'img': 'https://ocw.mit.edu' + response.xpath('//img[contains(@itemprop, "image")]/@src').extract()[0]

        }
