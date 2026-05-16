from pydantic import BaseModel, ConfigDict, Field


class RouteGenerateRequest(BaseModel):
    start_label: str = Field(min_length=1, max_length=150)
    target_distance_km: float = Field(gt=0, le=100)
    route_type: str = Field(min_length=1, max_length=30)
    environment: str = Field(min_length=1, max_length=50)


class RoutePlanResponse(BaseModel):
    id: int
    user_id: int
    start_label: str
    target_distance_km: float
    route_type: str
    environment: str
    center_lat: float
    center_lng: float
    path_json: str
    estimated_minutes: int
    safety_level: str
    summary: str

    model_config = ConfigDict(from_attributes=True)
