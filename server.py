import json
from mcp.server.fastmcp import Context
from typing import Optional, Dict, Any, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from mcp.server.fastmcp import FastMCP

from odoo_client import get_odoo_client


mcp = FastMCP(
    "Odoo MCP Server",
    description="MCP server for AI-based Odoo accounting tools",
)


app = FastAPI(title="Odoo Accounting MCP Server")

# CORS (Claude Desktop needs this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # loosen for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/mcp/odoo/accounting")
def get_account_moves():
    client = get_odoo_client()
    records = client.search_read(
        model="account.move",
        domain=[["state", "=", "posted"]],
        fields=["name", "date", "journal_id", "amount_total"],
        limit=10
    )
    return {"records": records}



@mcp.tool(description="Get recent journal entries for AI audit")
def get_recent_journal_entries(
    ctx: Context,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Fetches recent journal entries (account.move) for AI analysis.
    Allows optional filtering by date.
    """
    odoo = ctx.request_context.lifespan_context.odoo

    domain = [["state", "=", "posted"]]
    if start_date:
        domain.append(["date", ">=", start_date])
    if end_date:
        domain.append(["date", "<=", end_date])

    try:
        results = odoo.search_read(
            model_name="account.move",
            domain=domain,
            fields=["name", "date", "move_type", "amount_total", "journal_id", "partner_id"],
            limit=limit
        )
        return {"success": True, "result": results}
    except Exception as e:
        return {"success": False, "error": str(e)}
    

def main():
    uvicorn.run(app, host="0.0.0.0", port=8002)
