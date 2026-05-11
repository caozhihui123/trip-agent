"""LangGraph StateGraph 构建 — 连线 7 个节点"""
from langgraph.graph import StateGraph, START, END
from app.agents.state import TripPlannerState
from app.agents.nodes.init_node import init_node
from app.agents.nodes.poi_search_node import create_poi_search_node
from app.agents.nodes.weather_node import create_weather_node
from app.agents.nodes.route_planning_node import create_route_planning_node
from app.agents.nodes.compile_node import compile_node
from app.agents.nodes.budget_node import budget_node


def build_trip_planner_graph(tools_by_name: dict) -> StateGraph:
    """构建并编译旅行规划 LangGraph 工作流

    workflow: START → init → poi_search ──→ route_planning → compile → budget → END
                           → weather ────→
    """
    builder = StateGraph(TripPlannerState)

    # 创建工具绑定的 Agent 节点
    poi_node = create_poi_search_node(tools_by_name["amap_text_search"])
    weather_fn = create_weather_node(tools_by_name["amap_weather"])
    route_node = create_route_planning_node(tools_by_name["amap_route"])

    # 添加节点
    builder.add_node("init", init_node)
    builder.add_node("poi_search", poi_node)
    builder.add_node("weather", weather_fn)
    builder.add_node("route_planning", route_node)
    builder.add_node("compile", compile_node)
    builder.add_node("budget", budget_node)

    # 连线 — fan-out / fan-in
    builder.add_edge(START, "init")
    builder.add_edge("init", "poi_search")
    builder.add_edge("init", "weather")

    # route_planning 等待 poi_search 和 weather 都完成
    builder.add_edge("poi_search", "route_planning")
    builder.add_edge("weather", "route_planning")

    builder.add_edge("route_planning", "compile")
    builder.add_edge("compile", "budget")
    builder.add_edge("budget", END)

    return builder.compile()
