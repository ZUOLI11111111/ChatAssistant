import asyncio
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.tools.Config import Config, config
from app.tools.Base import BaseTool, ToolResult
from app.tools.BaseSearch import SearchItem, WebSearchEngine
from app.tools.BingSearch import BingSearchEngine
from app.tools.BaiduSearch import BaiduSearchEngine

class SearchResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    position: int = Field(description="Position in search results")
    url: str = Field(description="URL of the search result")
    title: str = Field(default="", description="Title of the search result")
    description: str = Field(default="", description="Description or snippet of the search result")
    source: str = Field(description="The search engine that provided this result")
    raw_content: Optional[str] = Field(default=None, description="Raw content from the search result page if available")

class SearchMetadata(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    total_results: int = Field(description="Total number of results found")
    language: str = Field(description="Language code used for the search")
    country: str = Field(description="Country code used for the search")

class SearchResponse(ToolResult):
    query: str = Field(description="The search query that was executed")
    results: List[SearchResult] = Field(default_factory=list, description="List of search results")
    metadata: Optional[SearchMetadata] = Field(default=None, description="Metadata about the search")

    @model_validator(mode="after")
    def PO(self) -> "SearchResponse":
        if self.error:
            return self
        result_text = [f"Search results for '{self.query}':"]
        for i, result in enumerate(self.results, 1):
            title = result.title.strip() or "No title"
            result_text.append(f"\n{i}.{title}")
            result_text.append(f"   URL: {result.url}")
            if result.description.strip():
                result_text.append(f"   Description: {result.description}")
            if result.raw_content:
                content = result.raw_content[:1000].replace("\n", " ").strip()
                if len(result.raw_content) > 1000:
                    content += "..."
                result_text.append(f"   Content: {content}")
        if self.metadata:
            result_text.extend(
                [
                    f"f\nMatadata:",
                    f"- Total results: {self.metadata.total_results}",
                    f"- Language: {self.metadata.language}",
                    f"-Country: {self.metadata.country}",
                ]
            )
        self.output = "\n".join(result_text)
        return self

class WebContentFetcher:
    @staticmethod
    async def FetchContent(url: str, timeout: int = 20) -> Optional[str]:
        headers = {"WebSearch": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        try:
            response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url, headers=headers, timeout=timeout))
            if response.status_code != 200:
                print(f"[ERROR] Failed to fetch content from {url}: HTTP {response.status_code}")
                return None
            soup = BeautifulSoup(response.text, "html.parser")
            for t in soup(["script", "style", "header", "footer", "nav"]):
                t.extract()
            text = soup.get_text(separator="\n", strip=True)
            text = " ".join(text.split())
            return text[:10000] if text else None
        except Exception as e:
            print(f"[ERROR] Fetching content from {url}: {e}")
            return None    

class WebSearch(BaseTool):
    name: str = "web_search"
    description: str = """Search the web for real-time information about any topic.
    This tool returns comprehensive search results with relevant information, URLs, titles, and descriptions.
    If the primary search engine fails, it automatically falls back to alternative engines."""
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "(required) The search query to submit to the search engine.",
            },
            "num_results": {
                "type": "integer",
                "description": "(optional) The number of search results to return. Default is 5.",
                "default": 5,
            },
            "lang": {
                "type": "string",
                "description": "(optional) Language code for search results (default: en).",
                "default": "zh",
            },
            "country": {
                "type": "string",
                "description": "(optional) Country code for search results (default: us).",
                "default": "cn",
            },
            "fetch_content": {
                "type": "boolean",
                "description": "(optional) Whether to fetch full content from result pages. Default is false.",
                "default": False,
            },
        },
        "required": ["query"],
    }
    _search_engine: dict[str, WebSearchEngine] = {"baidu": BaiduSearchEngine(), "bing": BingSearchEngine(),}
    content_fetcher: WebContentFetcher = WebContentFetcher()

    async def execute(self, query: str, num_results: int = 5, lang: Optional[str] = None, country: Optional[str] = None, fetch_content: bool = False,) -> SearchResponse:
        retry_delay = (getattr(config.search_config))
        