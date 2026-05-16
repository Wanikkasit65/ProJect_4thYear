from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.contact import EmergencyContactCreate, EmergencyContactResponse
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("", response_model=UserResponse)
def get_me(
    current_user=Depends(get_current_user),
) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.put("", response_model=UserResponse)
def update_me(
    payload: UserUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserResponse:
    service = UserService(db)
    user = service.update_user(current_user, payload)
    return UserResponse.model_validate(user)


@router.get("/emergency-contacts", response_model=list[EmergencyContactResponse])
def list_emergency_contacts(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[EmergencyContactResponse]:
    service = UserService(db)
    contacts = service.list_contacts(current_user.id)
    return [EmergencyContactResponse.model_validate(contact) for contact in contacts]


@router.post("/emergency-contacts", response_model=EmergencyContactResponse, status_code=201)
def create_emergency_contact(
    payload: EmergencyContactCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> EmergencyContactResponse:
    service = UserService(db)
    contact = service.create_contact(current_user.id, payload)
    return EmergencyContactResponse.model_validate(contact)
