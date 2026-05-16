"""create route plans

Revision ID: 20260417_0003
Revises: 20260417_0002
Create Date: 2026-04-17 05:20:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260417_0003"
down_revision = "20260417_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "route_plans",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("start_label", sa.String(length=150), nullable=False),
        sa.Column("target_distance_km", sa.Float(), nullable=False),
        sa.Column("route_type", sa.String(length=30), nullable=False),
        sa.Column("environment", sa.String(length=50), nullable=False),
        sa.Column("estimated_minutes", sa.Integer(), nullable=False),
        sa.Column("safety_level", sa.String(length=20), nullable=False),
        sa.Column("summary", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index(op.f("ix_route_plans_id"), "route_plans", ["id"], unique=False)
    op.create_index(op.f("ix_route_plans_user_id"), "route_plans", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_route_plans_user_id"), table_name="route_plans")
    op.drop_index(op.f("ix_route_plans_id"), table_name="route_plans")
    op.drop_table("route_plans")
