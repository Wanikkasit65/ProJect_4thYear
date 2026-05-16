from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import TimestampMixin


class RoutePlan(TimestampMixin, Base):
    __tablename__ = "route_plans"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    start_label: Mapped[str] = mapped_column(String(150), nullable=False)
    target_distance_km: Mapped[float] = mapped_column(Float, nullable=False)
    route_type: Mapped[str] = mapped_column(String(30), nullable=False)
    environment: Mapped[str] = mapped_column(String(50), nullable=False)
    center_lat: Mapped[float] = mapped_column(Float, nullable=False)
    center_lng: Mapped[float] = mapped_column(Float, nullable=False)
    path_json: Mapped[str] = mapped_column(String(4000), nullable=False)
    estimated_minutes: Mapped[int] = mapped_column(nullable=False)
    safety_level: Mapped[str] = mapped_column(String(20), nullable=False)
    summary: Mapped[str] = mapped_column(String(255), nullable=False)

    user = relationship("User", back_populates="route_plans")
