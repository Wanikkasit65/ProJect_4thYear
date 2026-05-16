from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.route import RouteGenerateRequest, RoutePlanResponse
from app.services.auth_service import get_current_user
from app.services.route_service import RouteService

router = APIRouter()


@router.get("", response_model=list[RoutePlanResponse])
def list_routes(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[RoutePlanResponse]:
    service = RouteService(db)
    routes = service.list_routes(current_user.id)
    return [RoutePlanResponse.model_validate(route) for route in routes]


@router.post("/generate", response_model=RoutePlanResponse, status_code=201)
def generate_route(
    payload: RouteGenerateRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RoutePlanResponse:
    service = RouteService(db)
    route = service.generate_route(current_user, payload)
    return RoutePlanResponse.model_validate(route)

