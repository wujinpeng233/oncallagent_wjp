from pydantic import BaseModel, Field

class ServiceStatusRequest(BaseModel):
    service_name: str = Field(description="服务名称",min_length=1,max_length=100)

class RecentLogsRequest(BaseModel):
    service_name: str = Field(description="服务名称",min_length=1,max_length=100)

class AlertDetailRequest(BaseModel):
    alert_id: str = Field(description="告警ID",min_length=1,max_length=100)

class RunbookSearchRequest(BaseModel):
    query: str = Field(description="查询内容",min_length=1,max_length=100)
