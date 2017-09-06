# -*- coding: utf-8 -*-

import scrapy
import json
import re


class EdxSpider(scrapy.Spider):
    name = 'edx'
    custom_settings = {
        'ITEM_PIPELINES': {
            'courses_grabber.pipelines.Courses_grabberPipeline': 400
        }
    }

    start_urls = ['https://www.edx.org/api/catalog/v2/courses']

    def parse(self, response):
        data = json.loads(response.text)
        for item in data["items"]:
            instructors = {}
            for lector in item['staff']:
                instructors[lector['title']] = str(lector['display_position']['title']) + ', ' + str(lector['display_position']['org'])
            duration = item['length']
            if 'hours' in duration:
                duration_filter = 'Less than a week'
            elif 'days' in duration:
                try:
                    duration_filter = int(int((re.findall('\d+', duration[0]))[0]) / 7)
                except ValueError:
                    duration_filter = None
            else:
                try:
                    duration_filter = (re.findall('\d+', duration[0]))[0]
                except IndexError:
                    duration_filter = None
            if isinstance(duration_filter, int) and duration_filter == 0:
                duration_filter = 'Less than a week'
            elif isinstance(duration_filter, int) and duration_filter > 12:
                duration_filter = 'More than 12 weeks'
            yield {
                'name': item['title'],
                'source': 'edx',
                'category': item['subjects'][0]['title'],
                'provider': item['schools'][0]['name'],
                'language': list(item['languages'].values())[0]['title'],
                'duration': duration,
                'duration_filter': duration_filter,
                'instructors_list': instructors,
                'start_date': item['start'],
                'description': item['description'],
                'link': 'https://www.edx.org/' + item['course_about_uri'],
                'img': item['image'],
                'video': item['video']['url']

            }
  
