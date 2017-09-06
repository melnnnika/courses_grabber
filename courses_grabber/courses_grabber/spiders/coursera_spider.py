import scrapy


class CourseraSpider(scrapy.Spider):
    name = 'coursera'

    start_urls = ['https://www.coursera.org/browse/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'courses_grabber.pipelines.Courses_grabberPipeline': 400
        }
    }

    def parse(self, response):
        for href in response.xpath('//a[contains(@class, "rc-DomainNavItem")]/@href').extract():
            yield scrapy.Request(response.urljoin(href),
                                callback=self.parse_category)

    def parse_category(self, response):
        subacategory_hrefs = response.xpath('//div[contains(@class, "bt3-text-center")]/a/@href').extract()
        if not subacategory_hrefs:
            course_hrefs = response.xpath('//a[contains(@class, "rc-OfferingCard")]/@href').extract()
            for href in course_hrefs:
                yield scrapy.Request(response.urljoin(href),
                                callback=self.parse_course)
        for href in subacategory_hrefs:
            yield scrapy.Request(response.urljoin(href),
                                callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        course_hrefs = response.xpath('//a[contains(@class, "rc-OfferingCard") and contains(@href, "learn/")]/@href').extract()
        for href in course_hrefs:
            yield scrapy.Request(response.urljoin(href),
                                callback=self.parse_course)

    def parse_course(self, response):
        provider = response.xpath('//div[contains(@class, "creator-names")]/span/text()').extract()
        language = response.xpath('//div[contains(@class, "rc-Language")]/text()').extract()
        instructors_list = {}
        for instructor, info in zip(response.xpath('//span[contains(@class, "body-1-text")]/a/text()').extract(), response.xpath('(//span[contains(@class, "body-1-text")]/text())[1]').extract()):
            instructors_list[instructor] = info.strip(',')
        duration = len(response.xpath('//div[contains(@class, "week-heading")]').extract())
        try:
            duration_filter = int(duration)
        except ValueError:
            duration_filter = None
        if duration_filter == 0:
            duration_filter = 'Less than a week'
        elif duration_filter > 12:
            duration_filter = 'More than 12 weeks'
        yield {
            'name': response.xpath('(//h2[contains(@class, "headline-4-text course-title")]/text()) | (//h2[contains(@class, "s12n-headline display-6-text")]/text())').extract()[0],
            'source': 'coursera',
            'provider': None if not provider else provider[1],
            'language': None if not language else language[0],
            'duration': duration,
            'duration_filter': duration_filter,
            'instructors_list': instructors_list,
            'start_date': response.xpath('//div[contains(@class, "startdate rc-StartDateString caption-text")]/span/text()').extract()[0],
            'description': response.xpath('(//p[contains(@class, "course-description")]/text()) |(//div[contains(@class, "description subsection")]//p/text())').extract()[0],
            'link': response.url,
            'video': None,
            'img': response.xpath('//div[contains(@class, "body-container")]/@style').extract()[0].split('(')[1].split(')')[0],
            'category': response.xpath('//div[contains(@class, "rc-BannerBreadcrumbs caption-text")]/span[2]//text()').extract()[0]
        }
        
