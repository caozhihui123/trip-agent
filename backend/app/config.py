"""配置管理 — 从环境变量读取所有配置"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")

# 高德
AMAP_API_KEY = os.getenv("AMAP_MAPS_API_KEY", "")
