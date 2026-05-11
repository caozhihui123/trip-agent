"""Amap MCP 工具 — FastMCP 服务 + LangChain @tool 双导出"""
import json
import httpx
from mcp.server.fastmcp import FastMCP
from langchain_core.tools import tool
from app.config import AMAP_API_KEY

BASE_URL = "https://restapi.amap.com/v3"

# ====== FastMCP 实例 ======
mcp = FastMCP("AmapTripTools")

# ====== 工具实现 ======

async def _do_text_search(keywords: str, city: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/place/text", params={
            "key": AMAP_API_KEY, "keywords": keywords, "city": city,
        }, timeout=10)
        data = resp.json()
        pois = data.get("pois", [])
        summary = [{"name": p["name"], "address": p.get("address", ""),
                    "location": p.get("location", ""), "id": p.get("id", "")}
                   for p in pois[:10]]
        return json.dumps(summary, ensure_ascii=False)


async def _do_weather(city: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/weather/weatherInfo", params={
            "key": AMAP_API_KEY, "city": city, "extensions": "all",
        }, timeout=10)
        data = resp.json()
        forecasts = data.get("forecasts", [{}])[0]
        casts = forecasts.get("casts", [])
        summary = [{"date": c["date"], "day_weather": c.get("dayweather", ""),
                    "night_weather": c.get("nightweather", ""),
                    "day_temp": c.get("daytemp", ""), "night_temp": c.get("nighttemp", "")}
                   for c in casts]
        return json.dumps(summary, ensure_ascii=False)


async def _do_route(origin: str, destination: str, mode: str, city: str) -> str:
    endpoints = {
        "walking": "direction/walking",
        "driving": "direction/driving",
        "transit": "direction/transit/integrated",
    }
    path = endpoints.get(mode, "direction/walking")
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/{path}", params={
            "key": AMAP_API_KEY, "origin": origin, "destination": destination, "city": city,
        }, timeout=10)
        data = resp.json()
        route_data = data.get("route", {})
        paths = route_data.get("paths", [])
        if paths:
            p = paths[0]
            return json.dumps({"distance": p.get("distance", ""),
                               "duration": p.get("duration", ""), "mode": mode}, ensure_ascii=False)
        return json.dumps({"error": "No route found"})


async def _do_geocode(address: str, city: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/geocode/geo", params={
            "key": AMAP_API_KEY, "address": address, "city": city,
        }, timeout=10)
        return json.dumps(resp.json(), ensure_ascii=False)


# ====== FastMCP 工具注册 ======

@mcp.tool()
async def amap_text_search(keywords: str, city: str) -> str:
    """搜索高德地图 POI（景点、餐厅、酒店等）。

    Args:
        keywords: 搜索关键词，如"热门景点"、"火锅"、"四星酒店"
        city: 城市名称，如"北京"、"杭州"
    """
    return await _do_text_search(keywords, city)


@mcp.tool()
async def amap_weather(city: str) -> str:
    """查询城市天气预报。

    Args:
        city: 城市名称
    """
    return await _do_weather(city)


@mcp.tool()
async def amap_route(origin: str, destination: str, mode: str = "walking", city: str = "") -> str:
    """规划两地之间的路线。

    Args:
        origin: 起点地址或位置
        destination: 终点地址或位置
        mode: 交通方式 - walking/driving/transit
        city: 城市名称
    """
    return await _do_route(origin, destination, mode, city)


@mcp.tool()
async def amap_geocode(address: str, city: str = "") -> str:
    """将地址转换为经纬度坐标。

    Args:
        address: 地址文本
        city: 城市名称（可选）
    """
    return await _do_geocode(address, city)


# ====== LangChain @tool 导出 ======

@tool
async def amap_text_search_tool(keywords: str, city: str) -> str:
    """搜索高德地图POI（景点、餐厅、酒店等）。参数: keywords(搜索关键词), city(城市名如'杭州')"""
    return await _do_text_search(keywords, city)


@tool
async def amap_weather_tool(city: str) -> str:
    """查询城市天气预报。参数: city(城市名)"""
    return await _do_weather(city)


@tool
async def amap_route_tool(origin: str, destination: str, mode: str = "walking", city: str = "") -> str:
    """规划两地之间路线。参数: origin(起点地址), destination(终点地址), mode(walking/driving/transit), city(城市名)"""
    return await _do_route(origin, destination, mode, city)


@tool
async def amap_geocode_tool(address: str, city: str = "") -> str:
    """将地址转换为经纬度。参数: address(地址文本), city(城市名)"""
    return await _do_geocode(address, city)


def get_tools_by_name() -> dict:
    """返回 name → LangChain BaseTool 的映射，供 Graph 构建使用"""
    return {
        "amap_text_search": amap_text_search_tool,
        "amap_weather": amap_weather_tool,
        "amap_route": amap_route_tool,
        "amap_geocode": amap_geocode_tool,
    }
