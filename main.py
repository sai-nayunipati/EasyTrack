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
        "sections.json": {"format": "json",
                          "overwrite": True},
    },
})

# process.crawl(CatalogSpider)
# process.start()

with open('sections.json', 'r', encoding='utf-8') as file_object:
    data = json.load(file_object)

dal.update_and_flag_sections_data(data)


# Have a table of sections found in the old scrape
# Create a table of sections found in the new scrape (the flag is true if the section goes from unavailable to available)
# Compare the two tables and update the old table with the new table

# See if users are tracking any sections that are no longer in the catalog. Remove them from the table.
# See if users are tracking any sections that just got flagged as available. Notify them.

"""
def refresh():
    pass


refresh()
"""
