import logging
from xml.etree import ElementTree


DC_NAMESPACE = {'dc': 'http://purl.org/dc/elements/1.1/'}
A10_NAMESPACE = {'a10': 'http://www.w3.org/2005/Atom'}


def parse_xml(xml_tree: ElementTree):
    rss_dict = {
        "channel_title": find_and_get_text(xml_tree, "channel/title"),
        "channel_link": find_and_get_text(xml_tree, "channel/link"),
        "channel_description": find_and_get_text(xml_tree, "channel/description"),
        "channel_copyright": find_and_get_text(xml_tree, "channel/copyright"),
        "channel_last_build_date": find_and_get_text(xml_tree, "channel/lastBuildDate"),
        "channel_ttl": find_and_get_text(xml_tree, "channel/ttl"),
        "items": []
    }

    channel_items = xml_tree.findall("channel/item")
    if channel_items is not None:
        for item in channel_items:
            item_dict = {
                "title": find_and_get_text(item, "title"),
                "description": find_and_get_text(item, "description"),
                "link": find_and_get_text(item, "link"),
                "guid": find_and_get_text(item, "guid"),
                "author": find_and_get_text(item, "a10:author/a10:name", A10_NAMESPACE),
                "pub_date": find_and_get_text(item, "pubDate"),
                "tags": find_and_get_text(item, "tags"),
                "subject": [sub.text for sub in item.findall('dc:subject', DC_NAMESPACE)],
                "enclosure": {
                    "url": find_and_get_attrib(item, "enclosure", "url"),
                    "type": find_and_get_attrib(item, "enclosure", "type"),
                    "length": find_and_get_attrib(item, "enclosure", "length")
                }
            }

            # check other some fields
            if not item_dict["author"]:
                item_dict["author"] = find_and_get_text(item, "dc:creator", DC_NAMESPACE)

            if not item_dict["tags"]:
                item_dict["tags"] = [cat.text for cat in item.findall('category')]

            rss_dict["items"].append(item_dict)

    logging.debug(rss_dict)

    return rss_dict


def find_and_get_text(xml_tree: ElementTree, path, namespaces=None, default=""):
    if namespaces is None:
        namespaces = {}
    el = xml_tree.find(path, namespaces)
    if el is not None:
        return el.text
    else:
        return default


def find_and_get_attrib(xml_tree: ElementTree, path, key_attrib, namespaces=None, default=""):
    if namespaces is None:
        namespaces = {}
    el = xml_tree.find(path, namespaces)
    if el is not None:
        attr = el.attrib.get(key_attrib)
        if attr:
            return attr
        else:
            return default
    else:
        return default
