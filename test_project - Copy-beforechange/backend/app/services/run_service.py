from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.run import Run
from app.models.user import User
from app.schemas.run import RunFinish, RunStart


class RunService:
    def __init__(self, db: Session):
        self.db = db

    def start_run(self, user: User, payload: RunStart) -> Run:
        run = Run(
            user_id=user.id,
            status="active",
            started_at=datetime.now(timezone.utc),
            notes=payload.notes,
        )
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def finish_run(self, run_id: int, user: User, payload: RunFinish) -> Run:
        run = self.db.get(Run, run_id)
        if run is None or run.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")
        run.status = "finished"
        run.finished_at = datetime.now(timezone.utc)
        run.distance_km = payload.distance_km
        run.duration_seconds = payload.duration_seconds
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def list_runs(self, user_id: int) -> list[Run]:
        statement = select(Run).where(Run.user_id == user_id).order_by(Run.created_at.desc())
        return list(self.db.scalars(statement).all())

