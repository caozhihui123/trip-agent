"""地图查询 API"""
from fastapi import APIRouter, Query
from app.models.schemas import RouteRequest
from app.services import amap_service as amap

router = APIRouter(prefix="/api/map", tags=["map"])


@router.get("/poi/search")
async def search_poi(keywords: str = Query(...), city: str = Query("")):
    return await amap.text_search(keywords, city)


@router.get("/poi/{poi_id}")
async def poi_detail(poi_id: str):
    return await amap.poi_detail(poi_id)


@router.get("/weather")
async def get_weather(city: str = Query(...)):
    return await amap.weather(city)


@router.post("/route")
async def get_route(req: RouteRequest):
    return await amap.route(req.origin, req.destination, req.mode, req.city)


@router.get("/geocode")
async def geocode(address: str = Query(...), city: str = Query("")):
    return await amap.geocode(address, city)


@router.get("/distance")
async def calc_distance(origins: str = Query(...), destination: str = Query(...), type: str = Query("1")):
    return await amap.distance(origins, destination, type)
