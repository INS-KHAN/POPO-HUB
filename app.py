from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup as bs
from flask import Flask, jsonify, render_template, request


class FamousHumorCrawler:
    def __init__(self):
        self.list_url = {
            "hu": "http://m.humoruniv.com/board/list.html?table=pds&st=day&pg=",
            "dd": "https://www.dogdrip.net/dogdrip?sort_index=popular&page=",
            "tq": "https://theqoo.net/index.php?mid=hot&page=",
            "th": "https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=",
        }
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 10) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/108.0.5359.79 Mobile Safari/537.36"
            )
        }

    def get_list(self, site, page=0):

        if site == "hu":
            resp = requests.get(
                url=f"{self.list_url['hu']}{page}",
                headers=self.headers,
            )
            resp.encoding = "EUC-KR"
            soup = bs(resp.text, "html.parser")
            table = soup.select_one("#list_body")
            ids = [
                parse_qs(urlparse(x.attrs["href"]).query)["number"][0]
                for x in table.select("a.list_body_href")
            ]
            titles = [x.text for x in table.select("span.link_hover")]
            rslt = {}
            for i in range(len(titles)):
                rslt[i] = {
                    "id": ids[i],
                    "title": titles[i],
                }
            return rslt

        elif site == "dd":
            resp = requests.get(
                url=f"{self.list_url['dd']}{page + 1}",
                headers=self.headers,
                verify=False,
            )
            soup = bs(resp.text, "html.parser")
            links = soup.select(".ed .title-link")
            ids = [urlparse(x.attrs["href"]).path[9:] for x in links]
            titles = [x.text for x in links]
            rslt = {}
            for i in range(len(titles)):
                rslt[i] = {
                    "id": ids[i],
                    "title": titles[i],
                }
            return rslt

        elif site == "tq":
            resp = requests.get(
                url=f"{self.list_url['tq']}{page + 1}",
                headers=self.headers,
                verify=False,
            )
            soup = bs(resp.text, "html.parser")
            item_list = soup.select_one(".list")
            ids = [
                parse_qs(urlparse(x.attrs["href"]).query)["document_srl"][0]
                for x in item_list.select(".list-link")
            ]
            titles = [
                x.text for x in item_list.select("li.title span[class!='category']")
            ]
            rslt = {}
            for i in range(len(titles)):
                rslt[i] = {
                    "id": ids[i],
                    "title": titles[i],
                }
            return rslt

        elif site == "th":
            resp = requests.get(
                url=f"{self.list_url['th']}{page + 1}",
                headers=self.headers,
            )
            soup = bs(resp.text, "html.parser")
            links = soup.select("td.subject a")
            ids = [parse_qs(urlparse(x.attrs["href"]).query)["no"][0] for x in links]
            titles = [x.text for x in links]
            rslt = {}
            for i in range(len(titles)):
                rslt[i] = {
                    "id": ids[i],
                    "title": titles[i],
                }
            return rslt


fhc = FamousHumorCrawler()

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/list/")
def list():
    prmts = request.args.to_dict()
    return jsonify(fhc.get_list(prmts["site"], int(prmts["page"])))


if __name__ == "__main__":
    app.run(debug=True)
