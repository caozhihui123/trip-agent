"""预算重算节点 — 纯 Python，修正 AI 的计算误差"""
from app.agents.state import TripPlannerState


def budget_node(state: TripPlannerState) -> dict:
    """从 trip.py 提取的 recalculate_budget 逻辑"""
    plan = state.get("trip_plan") or {}
    error_val = state.get("error")
    if error_val or not plan or "error" in str(plan):
        return {}

    tickets = 0
    dining = 0
    hotel_total = 0

    schedule = plan.get("schedule", [])
    for day in schedule:
        for attr in day.get("attractions", []):
            tickets += float(attr.get("ticket_price", 0) or 0)
        for meal in day.get("meals", []):
            dining += float(meal.get("estimated_cost", 0) or 0)

    hotel = plan.get("hotel") or {}
    days = plan.get("days", 1)
    price_per_night = float(hotel.get("price_per_night", 0) or 0)
    hotel_total = price_per_night * days

    transportation = 0
    for day in schedule:
        for route in day.get("routes", []):
            mode = route.get("mode", "")
            dist_str = route.get("distance", "0")
            dist = float(''.join(c for c in str(dist_str) if c.isdigit() or c == '.')) if dist_str else 0
            if mode == "walking":
                transportation += 0
            elif mode == "transit":
                transportation += 4
            elif mode == "driving":
                transportation += min(dist * 2, 50)

    total = tickets + hotel_total + dining + transportation

    plan["budget"] = {
        "tickets": round(tickets, 2),
        "hotel": round(hotel_total, 2),
        "dining": round(dining, 2),
        "transportation": round(transportation, 2),
        "total": round(total, 2),
    }
    return {"trip_plan": plan}
