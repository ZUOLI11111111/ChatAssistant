import json
import threading
import tomllib
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

#不用调试
def GetProjectRoot() -> Path:
    return Path(__file__).resolve().parent.parent

project_root = GetProjectRoot()
workspace = project_root / "workspace"

#不用测试
class LLMSettings(BaseModel):
    model: str = Field(..., description="Model name")
    base_url: str = Field(..., description="API Base URL")
    api_key: str = Field(..., description="API key")
    max_tokens: int = Field(4096, description="Maximum number of tokens per request")
    max_input_tokens: Optional[int] = Field(None, description="Maximum input tokens to use across all requests(None for unlimited)")
    temperature: float = Field(1.0, description="Sampling temperature")
    api_type: str = Field(..., description="Azure, Openai, or Ollama")
    api_version: str = Field(..., description="Azure Openai version if AzureOpenai")


#不用测试
class ProxySettings(BaseModel):
    server: str  = Field(None, description="Proxy server address")
    username: Optional[str] = Field(None, description="Proxy username")
    password: Optional[str] = Field(None, description="Proxy password")

#不用测试
class SearchSettings(BaseModel):
    engine: str = Field(default="Bing", description="Search engine the llm to use")
    fallback_engines: List[str] = Field(default_factory=lambda: ["Bing", "Baidu"], description="Fallback search engines to try if the primary engine fails",)
    retry_delay: int = Field(default=60, description="Seconds to wait before retrying all engines after they all fail",)
    max_retires: int = Field(default=5, description="Maximum number of times to retry all engines when all fail",)
    lang: str = Field(default="zh", description="Language code for search results (e.g., en, zh, fr)",)
    country: str = Field(default="cn", description="Country code for search results (e.g., us, cn, uk)",)

#暂时不用测试
class Config:
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._config = None
                    self.LoadInitialConfig()
                    self._initialized = True

    @staticmethod
    def GetConfigPath() -> Path:
        config_path = project_root / "config" / "config.toml"
        return config_path
    
    def LoadConfig(self) -> dict:
        with self.GetConfigPath().open("rb") as f:
            return tomllib.load(f)
    
    def LoadInitialConfig(self):
        t = self.LoadConfig().get("llm", {})
        tt = { k: v for k, v in self.LoadConfig().get("llm", {}).items() }
        default_settings = {
            "model": t.get("model"),
            "base_url": t.get("base_url"),
            "api_key": t.get("api_key"),
            "max_tokens": t.get("max_tokens", 4096),
            "max_input_tokens": t.get("max_input_tokens"),
            "temperature": t.get("temperature", 1.0),
            "api_type": t.get("api_type", ""),
            "api_version": t.get("api_version", ""),
        }
        #print(default_settings)
        

Config().LoadInitialConfig()

