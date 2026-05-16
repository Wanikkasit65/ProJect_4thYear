from pydantic import BaseModel, ConfigDict, Field


class RunStart(BaseModel):
    notes: str | None = Field(default=None, max_length=255)


class RunFinish(BaseModel):
    distance_km: float = Field(ge=0)
    duration_seconds: int = Field(ge=0)


class RunResponse(BaseModel):
    id: int
    user_id: int
    status: str
    distance_km: float
    duration_seconds: int
    notes: str | None

    model_config = ConfigDict(from_attributes=True)

