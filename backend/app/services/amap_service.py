"""高德地图 REST API 直调服务 — 供前端查询使用"""
import httpx
from app.config import AMAP_API_KEY

BASE_URL = "https://restapi.amap.com/v3"


async def text_search(keywords: str, city: str = "") -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/place/text", params={
            "key": AMAP_API_KEY, "keywords": keywords, "city": city,
        })
        return resp.json()


async def poi_detail(poi_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/place/detail", params={
            "key": AMAP_API_KEY, "id": poi_id,
        })
        return resp.json()


async def weather(city: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/weather/weatherInfo", params={
            "key": AMAP_API_KEY, "city": city, "extensions": "all",
        })
        return resp.json()


async def geocode(address: str, city: str = "") -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/geocode/geo", params={
            "key": AMAP_API_KEY, "address": address, "city": city,
        })
        return resp.json()


async def route(origin: str, destination: str, mode: str, city: str = "") -> dict:
    endpoints = {
        "walking": "direction/walking",
        "driving": "direction/driving",
        "transit": "direction/transit/integrated",
    }
    path = endpoints.get(mode, "direction/driving")
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/{path}", params={
            "key": AMAP_API_KEY, "origin": origin, "destination": destination,
            "city": city,
        })
        return resp.json()


async def distance(origins: str, destination: str, type: str = "1") -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/distance", params={
            "key": AMAP_API_KEY, "origins": origins, "destination": destination,
            "type": type,
        })
        return resp.json()
