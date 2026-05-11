"""LangGraph 共享状态定义"""
from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class TripPlannerState(TypedDict):
    # 输入参数
    city: str
    start_date: str
    days: int
    budget: float
    preferences: list[str]
    transportation: str
    hotel_preference: str

    # 消息历史 (自动累加)
    messages: Annotated[list[BaseMessage], add_messages]

    # 各阶段累积结果
    poi_results: list[dict]
    weather_results: list[dict]
    route_results: list[dict]

    # 最终输出
    trip_plan: Optional[dict]
    error: Optional[str]
