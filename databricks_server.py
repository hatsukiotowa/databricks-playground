"""
Databricks AI Gateway - 一體化 Server
同時 serve HTML Playground + 代理 Databricks API 請求
只需開放一個 port，無 CORS 問題

使用方式：
  pip install fastapi uvicorn httpx --break-system-packages
  python3 databricks_server.py

開啟瀏覽器：http://<你的IP>:8080/
"""

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pathlib import Path
import uvicorn

DATABRICKS_BASE_URL = "https://adb-7405612280372506.6.azuredatabricks.net"
HOST = "0.0.0.0"
PORT = 8080

app = FastAPI(title="Databricks Playground Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 首頁：直接 serve Playground HTML ─────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def serve_playground():
    html_path = Path(__file__).parent / "databricks_playground.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))

# ── API 代理：轉發所有 /serving-endpoints/* 請求到 Databricks ─────────────
@app.api_route("/serving-endpoints/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_serving_endpoints(path: str, request: Request):
    target_url = f"{DATABRICKS_BASE_URL}/serving-endpoints/{path}"
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    body = await request.body()

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            params=dict(request.query_params),
        )

    excluded = {"content-encoding", "transfer-encoding", "connection"}
    resp_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded}

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=resp_headers,
        media_type=resp.headers.get("content-type"),
    )


if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════════════╗
║     Databricks Playground Server 已啟動      ║
╠══════════════════════════════════════════════╣
║  開啟瀏覽器：http://20.89.104.109:{PORT}      ║
╚══════════════════════════════════════════════╝
""")
    uvicorn.run(app, host=HOST, port=PORT)
