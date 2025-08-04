from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
#暂时不调试
class BaseTool(ABC, BaseModel):
    name: str
    description: str
    parameters: Optional[dict] = None
    
    class  Config:
        arbitrary_types_allowed = True
    
    @abstractmethod
    async def Execute(self, **kwargs) -> Any:
        pass
    def ToParam(self) -> Dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters":self.parameters,
            },
        }
#暂时不调试
class ToolResult(BaseModel):
    output: Any = Field(default=None)
    error: Optional[str] = Field(default=None)
    base64_image: Optional[str] = Field(default=None)
    system: Optional[str] = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
#暂时不调试
class CLIResult(ToolResult):
    pass
#暂时不调试
class ToolFailure(ToolResult):
    pass

   