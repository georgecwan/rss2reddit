from bs4 import BeautifulSoup

# Parses RSS Feed and returns the newest headline and URL
def find_newest_headline(xml_data):
    soup = BeautifulSoup(xml_data, 'lxml-xml')
    top_item = soup.find('item')
    title = top_item.title.get_text()
    link = top_item.link.get_text()
    guid = top_item.guid.get_text() if top_item.guid.get_text() != "" else link
    return title, link, guid
