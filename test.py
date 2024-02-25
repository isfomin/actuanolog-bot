import rss.provider as rss
import rss.parser as parser
import logging
import sys
import json

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


urls = [
    "https://www.finam.ru/analysis/nslent/rsspoint/",
    "https://1prime.ru/export/rss2/index.xml",
    "https://www.vedomosti.ru/rss/news.xml",
    "https://www.cbr.ru/rss/eventrss",
    "https://www.computerweekly.com/rss/RSS-Feed.xml",
    "https://www.itnews.com.au/RSS/rss.ashx",
    "https://vc.ru/rss",
    "https://www.securitylab.ru/_services/export/rss/news/",
    "https://www.securitylab.ru/_services/export/rss/vulnerabilities/",
    "https://habr.com/ru/rss/feed/a638d6dc8b985709c3672ea2e7e03fab/?fl=ru&types%5B%5D=article",
]


def run(index=None):
    if index:
        xml_tree = rss.get(urls[index])
        return parser.parse_xml(xml_tree)
    else:
        results = []
        for url in urls:
            xml_tree = rss.get(url)
            results.append(parser.parse_xml(xml_tree))
        return results


res = run(9)
print(res)
