"""行程规划 API — 接入 LangGraph 多 Agent 工作流"""
from fastapi import APIRouter, Request
from app.models.schemas import TripRequest, TripEditRequest

router = APIRouter(prefix="/api/trip", tags=["trip"])


@router.post("/plan")
async def plan_trip(req: TripRequest, request: Request):
    initial_state = {
        "city": req.city,
        "start_date": req.start_date.isoformat(),
        "days": req.days,
        "budget": req.budget,
        "preferences": req.preferences,
        "transportation": req.transportation,
        "hotel_preference": req.hotel_preference,
        "messages": [],
        "poi_results": [],
        "weather_results": [],
        "route_results": [],
        "trip_plan": None,
        "error": None,
    }

    graph = request.app.state.trip_graph
    result = await graph.ainvoke(initial_state)

    if result.get("error"):
        return {"error": result["error"]}
    return result.get("trip_plan", {})


@router.put("/plan/{plan_id}")
async def edit_trip(plan_id: str, req: TripEditRequest):
    return {"message": "行程编辑暂未实现", "plan_id": plan_id, "plan": req.plan}
