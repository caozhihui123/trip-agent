"""Pydantic 数据模型"""

from pydantic import BaseModel
from datetime import date
from typing import Optional


# ====== 请求 ======

class TripRequest(BaseModel):
    city: str
    start_date: date
    days: int
    budget: float
    preferences: list[str] = []
    transportation: str = "driving"
    hotel_preference: str = "舒适型"


class TripEditRequest(BaseModel):
    plan: dict  # 完整的 TripPlan JSON


class RouteRequest(BaseModel):
    origin: str
    destination: str
    mode: str = "driving"
    city: str = ""


# ====== 响应 ======

class Attraction(BaseModel):
    name: str
    address: str = ""
    lng: float = 0
    lat: float = 0
    visit_duration: str = ""
    ticket_price: float = 0
    description: str = ""
    poi_id: Optional[str] = None


class Meal(BaseModel):
    restaurant: str
    address: str = ""
    lng: float = 0
    lat: float = 0
    meal_type: str = "午餐"
    estimated_cost: float = 0
    recommendation: str = ""


class Hotel(BaseModel):
    name: str
    address: str = ""
    lng: float = 0
    lat: float = 0
    price_per_night: float = 0
    rating: str = ""


class Route(BaseModel):
    from_place: str
    to_place: str
    mode: str = "walking"
    distance: str = ""
    duration: str = ""
    polyline: Optional[str] = None


class DayPlan(BaseModel):
    day: int
    date: str
    attractions: list[Attraction] = []
    meals: list[Meal] = []
    routes: list[Route] = []


class BudgetDetail(BaseModel):
    tickets: float = 0
    hotel: float = 0
    dining: float = 0
    transportation: float = 0
    total: float = 0


class TripPlan(BaseModel):
    city: str
    days: int
    schedule: list[DayPlan] = []
    hotel: Optional[Hotel] = None
    budget: BudgetDetail = BudgetDetail()
    weather: list[dict] = []
    tips: list[str] = []
