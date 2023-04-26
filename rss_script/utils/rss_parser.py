from typing import Tuple, Any

from bs4 import BeautifulSoup
from pprint import pprint


def find_newest_headline(xml_data) -> tuple[str, str, str] | tuple[None, None, None]:
    """
    Parses the XML data and returns the title, link, and guid of the newest headline

    Args:
        xml_data: XML data from the RSS feed to be parsed by BeautifulSoup

    Returns:
        A tuple of (title, link, guid) of the newest headline found in the XMl data
    """
    soup = BeautifulSoup(xml_data, 'lxml-xml')
    top_item = soup.find('item')
    try:
        title: str = top_item.title.get_text()
        link: str = top_item.link.get_text()
        guid: str = top_item.guid.get_text() if top_item.guid.get_text() != "" else link
        return title, link, guid
    except Exception as e:
        print(f"Error parsing RSS feed: {e}")
        print(f"XML Data:\n")
        pprint(soup)
        print("\n")
        return None, None, None