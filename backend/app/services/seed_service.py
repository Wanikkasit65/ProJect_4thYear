from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.role import Role
from app.models.user import User
from app.services.map_service import MapService
from app.services.security import hash_password


def seed_initial_data(db: Session) -> None:
    roles = list(db.scalars(select(Role)).all())
    if not roles:
        db.add_all(
            [
                Role(name="guest", description="Unauthenticated or limited-access user"),
                Role(name="member", description="Standard authenticated user"),
                Role(name="admin", description="Administrative user"),
            ]
        )
        db.commit()

    admin_role = db.scalar(select(Role).where(Role.name == "admin"))
    member_role = db.scalar(select(Role).where(Role.name == "member"))
    if admin_role is None or member_role is None:
        return

    # 🛡️ ดักจับความปลอดภัยของตัวแปรระบบ
    try:
        final_admin_email = getattr(settings, "ADMIN_EMAIL", getattr(settings, "admin_email", "admin@example.com"))
        final_admin_password = getattr(settings, "ADMIN_PASSWORD", getattr(settings, "admin_password", "admin1234"))
    except Exception:
        final_admin_email = "admin@example.com"
        final_admin_password = "admin1234"

    # 🛡️ ปรับตรรกะใหม่: ดักเช็กเลยว่าถ้าในระบบมีอีเมลนี้ หรือมี Username นี้อยู่แล้ว ห้ามกด INSERT ซ้ำเด็ดขาด
    admin_user = db.scalar(
        select(User).where(
            or_(
                User.email == final_admin_email,
                User.username == "runna_admin"
            )
        )
    )
    
    if admin_user is None:
        admin_user = User(
            first_name="Runna",
            last_name="Admin",
            username="runna_admin",
            email=final_admin_email,
            password_hash=hash_password(final_admin_password),
            role_id=admin_role.id,
            province="Chiang Mai",
        )
        db.add(admin_user)
        db.commit()

    MapService(db).ensure_seed_map()