"""路线规划 Agent 节点 — bind_tools + 手动工具循环"""
import json
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from app.services.llm_service import create_chat_model
from app.agents.prompts import ROUTE_PLANNING_SYSTEM_PROMPT
from app.agents.state import TripPlannerState


def create_route_planning_node(tool):
    """工厂：返回路线规划节点函数"""

    async def route_planning_node(state: TripPlannerState) -> dict:
        if state.get("error"):
            return {}

        poi_results = state.get("poi_results", [])
        if not poi_results:
            return {"route_results": []}

        pois_text = json.dumps(poi_results, ensure_ascii=False, indent=2)
        route_task = f"""以下是在 {state['city']} 搜索到的 POI 列表：
{pois_text}

请规划景点之间的路线。对相邻的景点对使用 amap_route 工具查询路线。
交通方式偏好：{state.get('transportation', 'walking')}
城市：{state['city']}"""

        llm = create_chat_model().bind_tools([tool])
        messages = [
            SystemMessage(content=ROUTE_PLANNING_SYSTEM_PROMPT),
            HumanMessage(content=route_task),
        ]

        routes = []
        for _ in range(8):
            response = await llm.ainvoke(messages)
            messages.append(response)

            tool_calls = getattr(response, "tool_calls", []) or []
            if not tool_calls:
                break

            for tc in tool_calls:
                args = tc.get("args", {})
                result_str = await tool.ainvoke(args)
                try:
                    data = json.loads(result_str) if isinstance(result_str, str) else result_str
                    if isinstance(data, dict) and "distance" in data:
                        routes.append(data)
                except (json.JSONDecodeError, TypeError):
                    pass
                messages.append(ToolMessage(content=str(result_str), tool_call_id=tc["id"]))

        return {"route_results": routes}

    return route_planning_node
