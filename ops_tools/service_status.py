MOCK_SERVICES ={
    "order-service":{
        "status":"degraded",
        "description":"订单服务异常，无法正常处理"
    },
    "mysql":{
        "status":"healthy",
        "description":"MySQL 库正常运行"
    },
    "redis": {
        "status": "degraded",
        "description": "模拟：Redis 请求延迟升高。",
    },
}

def get_service_status(service_name:str) -> dict:
    name = service_name.strip()

    if not name:
        raise ValueError("服务名称不能为空")

    service = MOCK_SERVICES.get(name)
    if service is None:
        raise ValueError(f"未找到服务：{name}")
    return {
        "service_name":name,
        "is_mock":True,
        **service,
    }