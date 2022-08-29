"""
This module refreshes every 20 minutes. Every refresh cycle it calls a spider,
resets the class database, and then updates any necessary users.
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from catalogscraper.catalogscraper.spiders.catalogspider import CatalogSpider

# Crawl BU's course catalog
process = CrawlerProcess(settings={
    "FEEDS": {
        "sections.json": {"format": "json",
                          "overwrite": True},
    },
})

process.crawl(CatalogSpider)
process.start()

# Update our database with the relevant information

"""
def refresh():
    pass


refresh()
"""
