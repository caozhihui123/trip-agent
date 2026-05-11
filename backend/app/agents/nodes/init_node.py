"""初始化节点 — 校验输入，准备初始消息"""
from langchain_core.messages import HumanMessage
from app.agents.state import TripPlannerState


def init_node(state: TripPlannerState) -> dict:
    """纯 Python 节点：校验输入参数，生成初始任务消息"""

    errors = []
    if not state.get("city"):
        errors.append("城市名不能为空")
    if state.get("days", 0) < 1 or state.get("days", 0) > 14:
        errors.append("天数需在1-14之间")
    if state.get("budget", 0) <= 0:
        errors.append("预算必须大于0")

    if errors:
        return {"error": "; ".join(errors)}

    task_msg = f"""请为我规划一次 {state['city']} 的 {state['days']} 天旅行：

第一步（POI搜索）：使用 amap_text_search 搜索 {state['city']} 的：
- 热门景点（搜索"热门景点"、"必去景点"、"公园"、"博物馆"）
- 餐厅（搜索"早餐"、"特色美食"、"本地菜"）
- 酒店（搜索"{state['hotel_preference']}酒店"）
搜索偏好：{", ".join(state['preferences']) if state.get('preferences') else "综合体验"}

第二步（天气查询）：使用 amap_weather 查询 {state['city']} 的天气预报。

第三步（路线规划）：基于找到的景点，使用 amap_route 规划相邻景点之间的路线。

旅行参数：
- 出发日期：{state['start_date']}
- 天数：{state['days']}
- 预算：{state['budget']} 元
- 交通方式：{state.get('transportation', 'walking')}
- 酒店偏好：{state.get('hotel_preference', '舒适型')}"""

    return {"messages": [HumanMessage(content=task_msg)]}
