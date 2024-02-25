import requests
import logging
from xml.etree.ElementTree import fromstring, ElementTree

rss_content_types = [
    'text/xml',
    'application/rss+xml',
    'application/xml'
]


def get(url: str, encoding="utf-8"):
    response = invoke_request(url)
    response.encoding = encoding

    try:
        xml_tree = ElementTree(fromstring(response.text))
    except BaseException as e:
        logging.error(e)
    else:
        return xml_tree


def invoke_request(url):
    try:
        response = requests.get(url)
    except BaseException as e:
        logging.warning(e)
    else:
        content_type = response.headers.get('content-type')

        if not content_type or prepare_content_type(content_type) not in rss_content_types:
            logging.warning(f"bad content-type=`{content_type}` is not one of {rss_content_types} for url {url}")

        return response


def prepare_content_type(content_type: str):
    parts = content_type.split(";")
    if len(parts) > 0:
        ct = parts[0]
        return ct
    return ""
