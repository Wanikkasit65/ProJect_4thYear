from sqlalchemy.orm import Session

from app.models.emergency_contact import EmergencyContact
from app.models.user import User
from app.schemas.contact import EmergencyContactCreate
from app.schemas.user import UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def update_user(self, user: User, payload: UserUpdate) -> User:
        if payload.first_name is not None:
            user.first_name = payload.first_name
        if payload.last_name is not None:
            user.last_name = payload.last_name
        if payload.province is not None:
            user.province = payload.province
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def list_contacts(self, user_id: int) -> list[EmergencyContact]:
        return (
            self.db.query(EmergencyContact)
            .filter(EmergencyContact.user_id == user_id)
            .order_by(EmergencyContact.created_at.desc())
            .all()
        )

    def create_contact(self, user_id: int, payload: EmergencyContactCreate) -> EmergencyContact:
        contact = EmergencyContact(
            user_id=user_id,
            name=payload.name,
            phone_number=payload.phone_number,
            relationship_label=payload.relationship_label,
        )
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact
