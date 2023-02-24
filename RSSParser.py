from bs4 import BeautifulSoup
from markdownify import markdownify as md

# Parses RSS Feed and returns the newest headline and URL
def find_newest_headline(xml_data):
    soup = BeautifulSoup(xml_data, 'lxml-xml')
    top_item = soup.find('item')
    title = top_item.title.text
    link = top_item.link.text
    guid = top_item.guid.text if top_item.guid.text != "" else link
    return title, link, guid
