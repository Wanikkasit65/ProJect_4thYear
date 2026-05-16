from sqlalchemy import Boolean, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.base import TimestampMixin


class MapEdge(TimestampMixin, Base):
    __tablename__ = "map_edges"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    start_node_id: Mapped[int] = mapped_column(ForeignKey("map_nodes.id"), nullable=False, index=True)
    end_node_id: Mapped[int] = mapped_column(ForeignKey("map_nodes.id"), nullable=False, index=True)
    road_name: Mapped[str] = mapped_column(String(150), nullable=False)
    road_class: Mapped[str] = mapped_column(String(50), nullable=False)
    speed_limit_kph: Mapped[float] = mapped_column(Float, nullable=False)
    length_m: Mapped[float] = mapped_column(Float, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    is_forbidden: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    geometry_json: Mapped[str] = mapped_column(String(4000), nullable=False)

