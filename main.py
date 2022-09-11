"""
This module refreshes every 20 minutes. Every refresh cycle it calls a spider,
resets the class database, and then updates any necessary users.
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from catalogscraper.catalogscraper.spiders.catalogspider import CatalogSpider
import json
import dal

# Crawl BU's course catalog
process = CrawlerProcess(settings={
    "FEEDS": {
        "scrape_data.json": {"format": "json",
                             "overwrite": True},
    },
})

# process.crawl(CatalogSpider)
# process.start()

# Tell the DAL to update the database with the new scrape data
courses = []
sections = []

with open('scrape_data.json', 'r', encoding='utf-8') as file_object:
    data = json.load(file_object)

for item in data:
    if item['type'] == 'course':
        del item['type']
        courses.append(item)
    elif item['type'] == 'section':
        del item['type']
        sections.append(item)

dal.update_courses(courses)
dal.update_sections(sections)

print("Done updating.")
