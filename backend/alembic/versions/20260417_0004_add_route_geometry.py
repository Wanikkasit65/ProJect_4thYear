"""add route geometry

Revision ID: 20260417_0004
Revises: 20260417_0003
Create Date: 2026-04-17 05:45:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260417_0004"
down_revision = "20260417_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("route_plans", sa.Column("center_lat", sa.Float(), nullable=False, server_default="18.8059"))
    op.add_column("route_plans", sa.Column("center_lng", sa.Float(), nullable=False, server_default="98.9523"))
    op.add_column(
        "route_plans",
        sa.Column(
            "path_json",
            sa.String(length=4000),
            nullable=False,
            server_default='[{"lat":18.8059,"lng":98.9523},{"lat":18.811,"lng":98.96},{"lat":18.8059,"lng":98.9523}]',
        ),
    )


def downgrade() -> None:
    op.drop_column("route_plans", "path_json")
    op.drop_column("route_plans", "center_lng")
    op.drop_column("route_plans", "center_lat")
