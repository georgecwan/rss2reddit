from bs4 import BeautifulSoup
from pprint import pprint


# Parses RSS Feed and returns the newest headline and URL
def find_newest_headline(xml_data):
    soup = BeautifulSoup(xml_data, 'lxml-xml')
    top_item = soup.find('item')
    try:
        title = top_item.title.get_text()
        link = top_item.link.get_text()
        guid = top_item.guid.get_text() if top_item.guid.get_text() != "" else link
        return title, link, guid
    except Exception as e:
        print(f"Error parsing RSS feed: {e}")
        print(f"XML Data:\n")
        pprint(soup)
        print("\n")
        return None, None, None