from fastapi import APIRouter, HTTPException


from ops_tools.service_status import get_service_status
from ops_tools.recent_logs import get_recentlogs
from ops_tools.alert_detail import get_alert_detail
from ops_tools.run_book import search_runbook

from schemas.tools import ServiceStatusRequest, RecentLogsRequest, AlertDetailRequest, RunbookSearchRequest


router = APIRouter(prefix="/tools",tags=["tools"])

@router.post("/service-status")
def query_service_status(data: ServiceStatusRequest):
    try:
        result = get_service_status(data.service_name)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )from exc

    return {
        "tool_name":"get_service-status",
        "arguments":{
            "service_name":data.service_name,
        },
        "result":result,

    }

@router.post("/recent-logs")
def query_recent_logs(data: RecentLogsRequest):
    try:
        result = get_recentlogs(data.service_name)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )from exc

    return {
        "tool_name":"get_recent-logs",
        "arguments":{
            "service_name":data.service_name,
        },
        "result":result,
    }

@router.post("/alert-detail")
def query_alert_detail(data: AlertDetailRequest):
    try:
        result = get_alert_detail(data.alert_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )from exc

    return {
        "tool_name":"get_alert-detail",
        "arguments":{
            "alert_id":data.alert_id,
        },
        "result":result,
    }

@router.post("/search-runbook")
def query_runbook(data: RunbookSearchRequest):
    if not data.query.strip():
        raise HTTPException(
            status_code=400,
            detail="query cannot be empty"
        )

    try:
        result = search_runbook(data.query)
    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"search runbook failed: {str(exc)}"
        )from exc

    return {
        "tool_name":"search_runbook",
        "arguments":{
            "query":data.query,
        },
        "result":result,
    }
