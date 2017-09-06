# -*- coding: utf-8 -*-

import psycopg2

categories_dict = {
    'Arts and Humanities': 'Art & Culture',
    'Architecture': 'Art & Culture',
    'Literature': 'Art & Culture',
    'Biological Engineering': 'Biology & Life Sciences',
    'Biology': 'Biology & Life Sciences',
    'Business': 'Business & Management',
    'Chemical Engineering': 'Chemistry',
    'IT & Software': 'Computer Science',
    'Data Science': 'Data Analysis & Statistics',
    'Economics': 'Economics & Finance',
    'Teacher Training': 'Education & Teacher Training',
    'Nuclear Science and Engineering': 'Energy & Earth Sciences',
    'Earth, Atmospheric, and Planetary Sciences': 'Energy & Earth Sciences',
    'Physical Science and Engineering': 'Engineering',
    'Aeronautics and Astronautics': 'Engineering',
    'Engineering Systems Division': 'Engineering',
    'Electrical Engineering and Computer Science': 'Engineering',
    'Materials Science and Engineering': 'Engineering',
    'Mechanical Engineering': 'Engineering',
    'Science, Technology, and Society': 'Engineering',
    'Civil and Environmental Engineering': 'Environmental Studies',
    'Health & Fitness': 'Health & Safety',
    'Athletics': 'Health & Safety',
    'Physical Education and Recreation': 'Health & Safety',
    'Health Sciences and Technology': 'Health & Safety',
    'Language Learning': 'Language',
    'Global Studies and Languages': 'Language',
    'Math and Logic': 'Math',
    'Mathematics': 'Math',
    'Comparative Media Studies': 'Media',
    'Comparative Media Studies/Writing': 'Media',
    'Media Arts and Sciences': 'Media',
    'Music and Theater Arts': 'Music and Theater',
    'Music': 'Music and Theater',
    'Urban Studies and Planning': 'Personal Development',
    'Political Science': 'Social Sciences'
}


class Courses_grabberPipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(host='', database='', user='', password='')
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        instructors_ids = []
        for key, value in item['instructors_list'].items():
            self.cursor.execute(
                """INSERT INTO courses_site_instructor (name, info)
                VALUES(%s, %s) RETURNING id;""",
                (key, value)
            )
            new_id = self.cursor.fetchone()[0]
            instructors_ids.append(new_id)

        category = categories_dict.get(item['category'], item['category'])
        if category:
            category = category.replace('&', 'and')
        self.cursor.execute(
            """INSERT INTO courses_site_course (name, source, provider, language, duration, duration_filter, start_date, link, description, category, image, video)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;""",
            (item['name'], item['source'], item['provider'], item['language'],  item['duration'], item['duration_filter'], item['start_date'], item['link'],  item['description'], category, item['img'], item['video'])
        )
        course_id = self.cursor.fetchone()[0]
        for i in instructors_ids:
            self.cursor.execute(
                """INSERT INTO courses_site_instructor_course (instructor_id, course_id)
                VALUES(%s, %s)""",
                (i, course_id)
            )
        self.connection.commit()
        return item
