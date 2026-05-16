from pydantic import BaseModel, ConfigDict, Field


class EmergencyContactCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    phone_number: str = Field(min_length=3, max_length=30)
    relationship_label: str | None = Field(default=None, max_length=100)


class EmergencyContactResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    relationship_label: str | None

    model_config = ConfigDict(from_attributes=True)

