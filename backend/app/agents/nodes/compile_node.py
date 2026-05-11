"""行程编译器节点 — LLM 直接调用生成最终 TripPlan JSON"""
import json
import re
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.llm_service import create_chat_model
from app.agents.prompts import COMPILER_SYSTEM_PROMPT
from app.agents.state import TripPlannerState


async def compile_node(state: TripPlannerState) -> dict:
    """纯 LLM 节点：读取所有累积数据，生成最终行程 JSON"""
    error_val = state.get("error")
    if error_val:
        return {}

    llm = create_chat_model(temperature=0.3)

    context = f"""## 已收集的数据

### POI 搜索结果
{json.dumps(state.get('poi_results', []), ensure_ascii=False, indent=2)}

### 天气预报
{json.dumps(state.get('weather_results', []), ensure_ascii=False, indent=2)}

### 路线规划
{json.dumps(state.get('route_results', []), ensure_ascii=False, indent=2)}

## 旅行参数
- 城市：{state['city']}
- 出发日期：{state['start_date']}
- 天数：{state['days']}
- 预算：{state['budget']} 元
- 偏好：{", ".join(state.get('preferences', []))}
- 交通方式：{state.get('transportation', 'walking')}
- 酒店偏好：{state.get('hotel_preference', '舒适型')}

请根据以上数据和输出格式要求，生成完整的旅行计划 JSON。"""

    messages = [
        SystemMessage(content=COMPILER_SYSTEM_PROMPT),
        HumanMessage(content=context),
    ]
    response = await llm.ainvoke(messages)
    raw = response.content

    # JSON 解析 — 与原 trip_planner.py 保持一致的容错逻辑
    json_match = re.search(r'```json\s*(.*?)\s*```', raw, re.DOTALL)
    if json_match:
        raw_json = json_match.group(1)
    else:
        start = raw.find('{')
        end = raw.rfind('}')
        if start != -1 and end != -1:
            raw_json = raw[start:end + 1]
        else:
            raw_json = raw

    try:
        trip_plan = json.loads(raw_json)
        return {"trip_plan": trip_plan}
    except json.JSONDecodeError:
        return {"error": f"Agent 返回格式解析失败", "trip_plan": {"raw": raw}}
