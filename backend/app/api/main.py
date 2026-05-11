"""FastAPI应用入口 — 多Agent LangGraph + MCP 架构"""
import sys
import io
import os
from contextlib import asynccontextmanager

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
os.environ.pop("SSL_CERT_FILE", None)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import trip, map
from app.mcp_server.amap_mcp import get_tools_by_name
from app.agents.graph_builder import build_trip_planner_graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动：加载 MCP/LangChain 工具 → 构建 Graph → 存到 app.state
    tools_by_name = get_tools_by_name()
    app.state.trip_graph = build_trip_planner_graph(tools_by_name)
    yield
    # 关闭：无特殊清理


app = FastAPI(title="智能旅行助手 API", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trip.router)
app.include_router(map.router)


@app.get("/")
def root():
    return {"message": "智能旅行助手 API v2.0 (LangGraph + MCP)", "docs": "/docs"}
