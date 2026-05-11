"""POI 搜索 Agent 节点 — 使用 bind_tools + 手动工具循环"""
import json
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from app.services.llm_service import create_chat_model
from app.agents.prompts import POI_SEARCH_SYSTEM_PROMPT
from app.agents.state import TripPlannerState


def create_poi_search_node(tool):
    """工厂：返回 POI 搜索节点函数"""

    async def poi_search_node(state: TripPlannerState) -> dict:
        if state.get("error"):
            return {}

        llm = create_chat_model().bind_tools([tool])
        messages = [SystemMessage(content=POI_SEARCH_SYSTEM_PROMPT),
                    HumanMessage(content=f"请搜索 {state['city']} 的景点、餐厅和酒店。"
                                 f"偏好：{', '.join(state.get('preferences', []))}。"
                                 f"酒店偏好：{state.get('hotel_preference', '舒适型')}。"
                                 f"请多次搜索不同关键词：热门景点、必去景点、公园、博物馆、"
                                 f"早餐、特色美食、本地菜、{state.get('hotel_preference', '舒适型')}酒店。")]

        all_pois = []
        for _ in range(10):
            response = await llm.ainvoke(messages)
            messages.append(response)

            tool_calls = getattr(response, "tool_calls", []) or []
            if not tool_calls:
                break

            for tc in tool_calls:
                args = tc.get("args", {})
                result_str = await tool.ainvoke(args)
                all_pois.extend(_parse_poi_result(result_str))
                messages.append(ToolMessage(content=str(result_str), tool_call_id=tc["id"]))

        return {"poi_results": all_pois}

    return poi_search_node


def _parse_poi_result(result_str) -> list[dict]:
    try:
        data = json.loads(result_str) if isinstance(result_str, str) else result_str
        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError, TypeError):
        return []
