from typing import List
from baidusearch.baidusearch import search
from app.tools.BaseSearch import SearchItem, WebSearchEngine

class BaiduSearchEngine(WebSearchEngine):
    def PerformSearch(self, query: str, num_results: int = 10, *args, **kwargs) -> List[SearchItem]:
        t = search(query, num_results= num_results)
        results = []
        for i, it in enumerate(t):
            if isinstance(i, str):
                results.append(SearchItem(title=f"Baidu Result {i + 1}", url = it, description=None))
            elif isinstance(it, dict):
                results.append(SearchItem(title=f"Baidu Result {i + 1}", url = it.get("url", ""), description=it.get("abstract", None)))
            else:
                try:
                    results.append(SearchItem(title=getattr(it, "title", f"Baidu Result {i + 1}"), url = getattr(it, "url", ""), description=getattr(it, "abstract", None)))
                except Exception:
                    results.append(SearchItem(title=f"Baidu Result {i + 1}", url = str(it), description=None))
        return results