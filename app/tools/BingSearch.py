from typing import List, Optional, Tuple
import requests
from bs4 import BeautifulSoup
from app.tools.BaseSearch import SearchItem, WebSearchEngine

ABSTRACT_MAX_LENGTH = 300

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-BR) AppleWebKit/533.3 (KHTML, like Gecko) QtWeb Internet Browser/3.7 http://www.QtWeb.net",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.4pre) Gecko/20070404 K-Ninja/2.1.3",
    "Mozilla/5.0 (Future Star Technologies Corp.; Star-Blade OS; x86_64; U; en-US) iNet Browser 4.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080414 Firefox/2.0.0.13 Pogo/2.0.0.13.6866",
]

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": USER_AGENTS[0],
    "Referer": "https://www.bing.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

BING_HOST_URL = "https://www.bing.com"
BING_SEARCH_URL = "https://www.bing.com/search?q="

class BingSearchEngine(WebSearchEngine):
    session: Optional[requests.Session] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def SearchSync(self, query: str, num_results: int = 10) -> List[SearchItem]:
        if not query:
            return []
        results = []
        next_url = BING_SEARCH_URL + query
        while len(results) < num_results:
            data, next_url = self.ParseHTML(next_url, start = len(results))
            if data:
                results.extend(data)
            if not next_url:
                break
        return results[:num_results]

    def ParseHTML(self, url: str, start: int = 0) -> Tuple[List[SearchItem], str]:
        try:
            res = self.session.get(url = url)
            res.encoding = "utf-8"
            root = BeautifulSoup(res.text, "lxml")
            list = []
            ol_results = root.find("ol", id = "b_results")
            if not ol_results:
                return [], None
            for li in ol_results.find_all("li", class_="b_algo"):
                title = ""
                url = ""
                abstract = ""
                try:
                    h2 = li.find("h2")
                    if h2:
                        title = h2.text.strip()
                        url = h2.a["href"].strip()
                    p = li.find("p")
                    if p:
                        abstract = p.text.strip()
                    if len(abstract) > ABSTRACT_MAX_LENGTH:
                        abstract = abstract[:ABSTRACT_MAX_LENGTH]
                    start += 1
                    list.append(SearchItem(title=title or f"Bing Result {start}", url = url, description=abstract))
                except Exception:
                    continue    
            next_btn = root.find("a", title="Next Page")
            if not next_btn:
                return list, None
            next_url = BING_HOST_URL + next_btn["href"]
            return list, next_url
        except Exception as e:
            print(f"[Warning] Error parsing HTML: {e}")
            return [],None

    def PerformSearch(self, query: str, num_results: int = 10, *args, **kwargs):
        return self.SearchSync(query, num_results=num_results)
    