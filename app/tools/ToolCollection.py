from typing import Any, Dict, List
from app.tools.Exceptions import ToolError
from app.tools.Base import BaseTool, ToolFailure, ToolResult

class ToolCollection:
    class Config:
        arbitrary_types_allowed = True

    def __init__(self, *tools: BaseTool):
        self.tools = tools
        self.tool_map = {tool.name: tool for tool in tools}

    def __iter__(self):
        return iter(self.tools)

    def ToParams(self) -> List[Dict[str, Any]]:
        return [tool.to_param() for tool in self.tools]

    async def Execute(self, *, name: str, tool_input: Dict[str, Any] = None) -> ToolResult:
        tool = self.tool_map.get(name)
        if not tool:
            return ToolFailure(error=f"Tool {name} is invalid")
        try:
            result = await tool(**tool_input)
            return result
        except ToolError as e:
            return ToolFailure(error=e.message)

    async def ExecuteAll(self) -> List[ToolResult]:
        results = []
        for tool in self.tools:
            try:
                result = await tool()
                results.append(result)
            except ToolError as e:
                results.append(ToolFailure(error=e.message))
    def GetTool(self, name: str) -> BaseTool:
        return self.tool_map.get(name)

    def AddTool(self, tool : BaseTool):
        if tool.name in self.tool_map:
            print(f"Tool {tool.name} already exists in collection, skipping.")
            return self
        self.tools += (tool,)
        self.tool_map[tool.name] = tool
        return self

    def AddTools(self, *tools: BaseTool):
        for tool in tools:
            self.AddTool(tool)
        return self
