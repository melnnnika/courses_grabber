# -*- coding: utf-8 -*-
import scrapy
import re


class EderaSpider(scrapy.Spider):
    name = 'edera'
    custom_settings = {
        'ITEM_PIPELINES': {
            'courses_grabber.pipelines.Courses_grabberPipeline': 400
        }
    }

    start_urls = ['https://www.ed-era.com/courses/']

    def parse(self, response):
        for href in response.xpath('(//div[contains(@id, "courses")])[2]//a[contains(@class, "button goto_course")]/@href').extract():
            yield scrapy.Request(response.urljoin(href),
                                callback=self.parse_course)

    def parse_course(self, response):
        instructors_list = {}
        for instructor, info in zip(response.xpath('//div[contains(@class, "photo")]/p/b/text()').extract(), response.xpath('//div[contains(@class, "main-staff-description")]/p[1]/text()').extract()):
            instructors_list[instructor] = info
        duration = response.xpath('(//ul[contains(@class, "features")]/li)[3]/text()').extract()[0]
        duration_filter = (re.findall('\d+', duration[0]))[0]
        yield {
            'name': response.xpath('(//h1/text())[3]').extract()[0].strip(),
            'source': 'edera',
            'category': None,
            'provider': None,
            'language': 'Українська',
            'duration': duration,
            'duration_filter': duration_filter,
            'instructors_list': instructors_list,
            'start_date': response.xpath('(//div[contains(@class, "info")]/ul/li/span)[1]/text()').extract()[0],
            'description': response.xpath('//div[contains(@class, "short-description")]/p/text()').extract()[0],
            'link': response.url,
            'img': response.xpath('//a[contains(@class, "popup-youtube")]/@style').extract()[0].split('\'')[1],
            'video': response.xpath('//a[contains(@class, "popup-youtube playBut")]/@href').extract()[0]
        }
