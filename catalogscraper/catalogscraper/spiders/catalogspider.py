"""
This module scans the public BU course catalog to populate the project
databse with its information.

This scrapy primer is highly recommended: https://www.youtube.com/watch?v=s4jtkzHhLzY
"""

import scrapy


class CatalogSpider(scrapy.Spider):
    name = 'catalog'

    # Incomplete, for testing
    start_urls = ['https://www.bu.edu/phpbin/course-search/search.php?page=w0&pagesize=10&adv=1&nolog=&search_adv_all=&yearsem_adv=2022-FALL&credits=*&pathway=&hub_match=all']
    # start_urls = ['https://www.bu.edu/phpbin/course-search/search.php?page=w0&pagesize=10&adv=1&nolog=&search_adv_all=&yearsem_adv=2022-FALL&credits=*&pathway=&hub_match=all&pagesize=-1']

    def parse(self, response):
        for search_result in response.css('li.coursearch-result'):
            # 'CAS AA 103' -> ['CAS', 'AA', '103']
            components = search_result.css('h6::text').get().split()

            yield {
                'type': 'course',
                'college': components[0],
                'department': components[1],
                'number': components[2],
            }

            sections_link = search_result.css(
                'a.coursearch-result-sections-link').attrib['href']

            yield response.follow('https://www.bu.edu' + sections_link, callback=self.parse_sections)

    def parse_sections(self, response):
        # Omit the header row
        sections = response.css('div.coursearch-course-section tr')[1:]

        components = response.css('h6::text').get().split()

        for row in sections:
            is_available = True
            class_notes = row.css('td:nth-child(8)').get()
            if ("Class Closed" in class_notes
                    or "Class Full" in class_notes):
                is_available = False

            yield {
                # 'CAS AA 103' -> ['CAS', 'AA', '103']
                'type': 'section',
                'college': components[0],
                'department': components[1],
                'number': components[2],
                'code': row.css('td:nth-child(1)::text').get().strip(),
                'is_available': is_available,
            }
