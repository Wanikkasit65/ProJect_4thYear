from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import TimestampMixin


class HazardMarker(TimestampMixin, Base):
    __tablename__ = "hazard_markers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    marker_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[int] = mapped_column(nullable=False, default=1)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lng: Mapped[float] = mapped_column(Float, nullable=False)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="approved")

    user = relationship("User", back_populates="hazard_markers")

