import sqlalchemy as sa
from sqlalchemy import Boolean, Float, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.base import TimestampMixin


class MapNode(TimestampMixin, Base):
    __tablename__ = "map_nodes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    osm_id: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lng: Mapped[float] = mapped_column(Float, nullable=False)
    is_intersection: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

