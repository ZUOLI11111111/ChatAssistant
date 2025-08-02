import asyncio
from typing import Any, Dict, List, Optional
import requests
from bs4  import BeautifulSoup
from pydantic import BaseModel, ConfigDict, Field, validate_model