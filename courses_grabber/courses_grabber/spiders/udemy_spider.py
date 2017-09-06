import scrapy
import json


class UdemySpider(scrapy.Spider):
    name = 'udemy'
    custom_settings = {
        'ITEM_PIPELINES': {
            'courses_grabber.pipelines.Courses_grabberPipeline': 400
        }
    }
    start_urls = ['https://www.udemy.com/courses/']

    def parse(self, response):
        for href in response.xpath('//ul[contains(@class, "menu__sub-list")]/li[position()>1]/a/@href').extract():
            yield scrapy.Request(
                response.urljoin(href + 'all-courses/'),
                callback=self.parse_category
            )

    def parse_category(self, response):
        category_id = response.xpath('substring-before(substring-after(//script[contains(text(), "UD.channel")]/text(), "id:"), ",")').extract()[0]
        category = response.xpath('substring-before(substring-after(normalize-space(//script[contains(text(), "UD.channel.parentChannel")]/text()), "UD.channel.parentChannel = { title: "), ",")').extract()[0]
        subcategory = response.xpath('substring-before(substring-after(//script[contains(text(), "UD.channel")]/text(), "title: "), ",")').extract()[0]
        url = 'https://www.udemy.com/api-2.0/channels/%s/courses' % (category_id.strip())
        yield scrapy.Request(
            url,
            meta={'category': category[1:-1], 'subcategory': subcategory[1:-1]},
            callback=self.parse_category_pages
        )

    def parse_category_pages(self, response):
        data = json.loads(response.text)
        for course in data["results"]:
            instructors = {}
            for lector in course['visible_instructors']:
                instructors[lector['title']] = lector['job_title']
            yield {
                'name': course['title'],
                'source': 'udemy',
                'category': response.meta['category'],
                'provider': None,
                'language': course['locale']['title'],
                'duration': course['content_info'],
                'duration_filter': 'Less than a week',
                'instructors_list': instructors,
                'start_date': course['published_time'],
                'description': None,
                'link': 'https://www.udemy.com' + course["url"],
                'video': None,
                'img': course['image_480x270']
            }
        if data['next']:
            yield scrapy.Request(
                data['next'],
                meta={'category': response.meta['category'], 'subcategory': response.meta['subcategory']},
                callback=self.parse_category_pages
            )
