# 智能旅行助手

AI 驱动的中国城市旅行规划工具，输入目的地、日期和偏好，自动生成包含景点、餐饮、酒店的完整行程，支持地图可视化和 PDF 导出。

## 功能特点

- **智能行程规划** — 基于 DeepSeek LLM + 高德地图，自动搜索真实景点、天气和路线，生成多日完整行程
- **地图可视化** — 高德地图标注景点位置，绘制游览路线，按天切换显示
- **预算计算** — 自动汇总门票、酒店、餐饮、交通费用，后端精确核算
- **行程切换** — 按天切换查看每日景点、路线和餐饮详情
- **导出功能** — 支持导出完整行程为 PDF 或图片

## 技术栈

### 后端
| 技术 | 用途 |
|------|------|
| Python 3.10 | 运行环境 |
| FastAPI | Web 框架 |
| HelloAgents | AI Agent 框架 (SimpleAgent + Tool) |
| DeepSeek | 大语言模型 (deepseek-chat) |
| 高德地图 API | POI 搜索、天气、路线规划 |
| Pydantic | 数据模型校验 |

### 前端
| 技术 | 用途 |
|------|------|
| Vue 3 + TypeScript | 前端框架 |
| Vite | 构建工具 |
| Ant Design Vue | UI 组件库 |
| 高德 JS API 2.0 | 地图展示 |
| html2canvas + jsPDF | PDF/图片导出 |
| Axios | HTTP 请求 |

## 项目结构

```
trip_agent/
├── backend/                        # 后端服务
│   ├── app/
│   │   ├── api/
│   │   │   ├── main.py             # FastAPI 入口，CORS 配置
│   │   │   └── routes/
│   │   │       ├── trip.py         # 行程规划 API + 预算核算
│   │   │       └── map.py          # 地图查询 API
│   │   ├── agents/
│   │   │   └── trip_planner.py     # TripPlannerAgent + 高德工具
│   │   ├── services/
│   │   │   ├── llm_service.py      # LLM 工厂
│   │   │   └── amap_service.py     # 高德 REST API 直调
│   │   ├── models/
│   │   │   └── schemas.py          # Pydantic 数据模型
│   │   └── config.py               # 环境变量读取
│   ├── requirements.txt
│   ├── .env.example                # 环境变量模板
│   └── .env                        # 实际环境变量（不提交）
│
└── frontend/                       # 前端应用
    ├── src/
    │   ├── components/
    │   │   ├── TripForm.vue        # 输入表单
    │   │   ├── TripResult.vue      # 结果容器（左右分栏）
    │   │   ├── MapPanel.vue        # 高德地图 + 路线
    │   │   ├── DayCard.vue         # 单日行程卡片
    │   │   ├── BudgetPanel.vue     # 预算明细
    │   │   └── ExportToolbar.vue   # PDF/图片导出
    │   ├── services/
    │   │   └── api.ts              # Axios API 客户端
    │   ├── types/
    │   │   └── index.ts            # TypeScript 类型定义
    │   └── main.ts                 # 入口文件
    ├── package.json
    └── vite.config.ts
```

## 环境配置

### 前提条件

- Anaconda3（已配置 py3.10 环境）
- Node.js 16+
- DeepSeek API Key
- 高德地图 Web 服务 API Key

### 1. 安装 Python 依赖

```bash
conda activate py3.10
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件，填入 API Key：

```env
LLM_API_KEY=你的DeepSeek_API_Key
LLM_MODEL=deepseek-chat
LLM_BASE_URL=https://api.deepseek.com/v1
AMAP_MAPS_API_KEY=你的高德_API_Key
```

### 3. 安装前端依赖

```bash
cd frontend
npm install
```

## 启动项目

### 启动后端（终端 1）

```bash
conda activate py3.10
set PYTHONIOENCODING=utf8          # Windows 需设置 UTF-8 编码
cd backend
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

后端运行在 `http://localhost:8000`，API 文档在 `http://localhost:8000/docs`。

### 启动前端（终端 2）

```bash
cd frontend
npm run dev
```

前端运行在 `http://localhost:5173`。

### 使用

打开 `http://localhost:5173`，填写以下信息：

1. **目的地城市** — 仅支持中国城市（如：杭州、成都、西安）
2. **出发日期** — 选择日期
3. **旅行天数** — 1-7 天
4. **预算** — 总预算（元）
5. **偏好** — 历史文化 / 自然风光 / 美食之旅 / 亲子游玩 / 网红打卡 / 购物休闲
6. **交通方式** — 自驾/打车 / 公共交通 / 混合
7. **酒店偏好** — 经济型 / 舒适型 / 豪华型

点击「生成旅行计划」，AI 会调用高德地图搜索真实数据，生成完成后在下方展示地图、行程卡片和预算明细。生成耗时约 30-90 秒。

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/trip/plan` | 生成行程计划 |
| PUT  | `/api/trip/plan/{id}` | 编辑行程 |
| GET  | `/api/map/poi/search` | 搜索 POI |
| GET  | `/api/map/poi/{id}` | POI 详情 |
| GET  | `/api/map/weather` | 天气查询 |
| POST | `/api/map/route` | 路线规划 |
| GET  | `/api/map/geocode` | 地理编码 |
| GET  | `/api/map/distance` | 距离计算 |
