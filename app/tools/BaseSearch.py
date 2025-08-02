from typing import List, Optional
from pydantic import BaseModel, Field

class SearchItem(BaseModel):
    title: str = Field(description="The title of the search result")
    url: str = Field(description="The URL of the search result")
    description: Optional[str] = Field(default=None, description="A description or snippet of the search result")
    def TitleAndURLString(self) -> str:
        return f"{self.title} - {self.url}"

class WebSearchEngine(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    def PerformSearch(self, query: str, num_results: int = 10, *args, **kwargs) -> List[SearchItem]:
        raise NotImplementedError