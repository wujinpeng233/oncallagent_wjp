MOCK_ALERTS = {
    "alert-001": {
        "service_name": "order-service",
        "severity": "critical",
        "title": "订单服务 HTTP 500 错误率升高",
        "description": "模拟：订单服务最近 5 分钟错误率超过阈值。",
    },
    "alert-002": {
        "service_name": "redis",
        "severity": "warning",
        "title": "Redis 请求超时",
        "description": "模拟：Redis 请求延迟升高，出现读取超时。",
    },
}

def get_alert_detail(alert_id: str) -> dict:
    alert_id = alert_id.strip()
    if not alert_id:
        raise ValueError("告警ID不能为空")
    alert = MOCK_ALERTS.get(alert_id)
    if alert is None:
        raise ValueError(f"告警 {alert_id} 不存在")
    return {
        "alert_id": alert_id,
        "is_mock": True,
        **alert,
    }
