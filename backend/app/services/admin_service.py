from sqlalchemy import select, update, and_
from sqlalchemy.orm import Session

from app.models.map_edge import MapEdge
from app.models.hazard_marker import HazardMarker
from app.models.user import User
from app.services.map_service import MapService


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def override_edge_risk(self, edge_id: int, risk_score: float, is_forbidden: bool = False) -> MapEdge:
        """Admin override for edge risk_score or forbidden status."""
        edge = self.db.get(MapEdge, edge_id)
        if not edge:
            raise ValueError("Edge not found")
        edge.risk_score = risk_score
        edge.is_forbidden = is_forbidden
        self.db.commit()
        self.db.refresh(edge)
        return edge

    def approve_hazard_marker(self, marker_id: int, approved: bool = True) -> HazardMarker:
        """Approve or reject hazard marker."""
        marker = self.db.get(HazardMarker, marker_id)
        if not marker:
            raise ValueError("Marker not found")
        marker.status = "approved" if approved else "rejected"
        self.db.commit()
        self.db.refresh(marker)
        return marker

    def list_high_risk_edges(self, risk_threshold: float = 0.8) -> list[MapEdge]:
        """List edges above risk threshold for admin review."""
        return list(self.db.scalars(
            select(MapEdge).where(MapEdge.risk_score > risk_threshold).order_by(MapEdge.risk_score.desc())
        ).all())

    def rebuild_map_graph(self) -> dict:
        """Trigger full map reimport."""
        MapService(self.db).import_osm_data(18.79, 98.94, 18.82, 98.97)
        self.db.commit()
        return {"status": "rebuilt"}

