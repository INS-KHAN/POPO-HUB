import warnings
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup as bs

warnings.filterwarnings(action="ignore")


class PopoCrawler:
    def __init__(self):
        self.list_url = {
            "hu": "http://m.humoruniv.com/board/list.html?table=pds&st=day&pg=",
            "dd": "https://www.dogdrip.net/dogdrip?sort_index=popular&page=",
            "tq": "https://theqoo.net/index.php?mid=hot&page=",
            "th": "https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=",
        }

    def get(self, url, verify=True, encoding=None):
        resp = requests.get(
            url=url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Linux; Android 10) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/108.0.5359.79 Mobile Safari/537.36"
                )
            },
            verify=verify,
        )
        if encoding:
            resp.encoding = "EUC-KR"
        return resp

    def lists2json(self, **kwargs):
        rslt = {}
        keys = list(kwargs.keys())
        values = list(kwargs.values())
        for i in range(len(values[0])):
            rslt[i] = dict(zip(keys, [x[i] for x in values]))
        return rslt

    def get_list(self, site, page=0):

        if site == "hu":
            resp = self.get(url=f"{self.list_url['hu']}{page}", encoding="EUC-KR")
            soup = bs(resp.text, "html.parser")
            table = soup.select_one("#list_body")
            ids = [
                parse_qs(urlparse(x.attrs["href"]).query)["number"][0]
                for x in table.select("a.list_body_href")
            ]
            titles = [x.text for x in table.select("span.link_hover")]
            return self.lists2json(title=titles, id=ids)

        elif site == "dd":
            resp = self.get(url=f"{self.list_url['dd']}{page + 1}", verify=False)
            soup = bs(resp.text, "html.parser")
            links = soup.select(".ed .title-link")
            ids = [urlparse(x.attrs["href"]).path[9:] for x in links]
            titles = [x.text for x in links]
            return self.lists2json(title=titles, id=ids)

        elif site == "tq":
            resp = self.get(url=f"{self.list_url['tq']}{page + 1}", verify=False)
            soup = bs(resp.text, "html.parser")
            item_list = soup.select_one(".list")
            ids = [
                parse_qs(urlparse(x.attrs["href"]).query)["document_srl"][0]
                for x in item_list.select(".list-link")
            ]
            titles = [
                x.text for x in item_list.select("li.title span[class!='category']")
            ]
            return self.lists2json(title=titles, id=ids)

        elif site == "th":
            resp = self.get(url=f"{self.list_url['th']}{page + 1}")
            soup = bs(resp.text, "html.parser")
            links = soup.select("td.subject a")
            ids = [parse_qs(urlparse(x.attrs["href"]).query)["no"][0] for x in links]
            titles = [x.text for x in links]
            return self.lists2json(title=titles, id=ids)
