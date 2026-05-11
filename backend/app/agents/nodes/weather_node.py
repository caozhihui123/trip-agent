"""天气查询 Agent 节点 — bind_tools + 手动工具循环"""
import json
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from app.services.llm_service import create_chat_model
from app.agents.prompts import WEATHER_SYSTEM_PROMPT
from app.agents.state import TripPlannerState


def create_weather_node(tool):
    """工厂：返回天气查询节点函数"""

    async def weather_node(state: TripPlannerState) -> dict:
        if state.get("error"):
            return {}

        llm = create_chat_model().bind_tools([tool])
        messages = [
            SystemMessage(content=WEATHER_SYSTEM_PROMPT),
            HumanMessage(content=f"请查询 {state['city']} 的天气预报"),
        ]

        weather_data = []
        for _ in range(4):
            response = await llm.ainvoke(messages)
            messages.append(response)

            tool_calls = getattr(response, "tool_calls", []) or []
            if not tool_calls:
                break

            for tc in tool_calls:
                args = tc.get("args", {})
                result_str = await tool.ainvoke(args)
                weather_data = _parse_weather_result(result_str)
                messages.append(ToolMessage(content=str(result_str), tool_call_id=tc["id"]))

        return {"weather_results": weather_data}

    return weather_node


def _parse_weather_result(result_str) -> list[dict]:
    try:
        data = json.loads(result_str) if isinstance(result_str, str) else result_str
        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError, TypeError):
        return []
