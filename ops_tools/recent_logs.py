MOCK_LOGS = {
    "order-service": [
        {
            "level": "ERROR",
            "message": "Database connection refused",
        },
        {
            "level": "ERROR",
            "message": "POST /orders returned HTTP 500",
        },
    ],
    "mysql": [
        {
            "level": "INFO",
            "message": "Database service is running",
        },
    ],
    "redis": [
        {
            "level": "WARN",
            "message": "Redis read timeout",
        },
    ],
}

def get_recentlogs(service_name: str) -> dict:
     name = service_name.strip()

     if not name:
         raise ValueError("服务名称不能为空")
     logs = MOCK_LOGS.get(name)

     if logs is None:
         raise ValueError(f"服务 {name} 不存在日志")
     return {
         "service_name":name,
         "is_mock":True,
         "logs":logs,
     }
