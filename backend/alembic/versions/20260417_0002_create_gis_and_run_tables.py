"""create gis and run tables

Revision ID: 20260417_0002
Revises: 20260417_0001
Create Date: 2026-04-17 04:20:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260417_0002"
down_revision = "20260417_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "map_nodes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=150), nullable=True),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("lng", sa.Float(), nullable=False),
        sa.Column("is_intersection", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f("ix_map_nodes_id"), "map_nodes", ["id"], unique=False)

    op.create_table(
        "map_edges",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("start_node_id", sa.Integer(), nullable=False),
        sa.Column("end_node_id", sa.Integer(), nullable=False),
        sa.Column("road_name", sa.String(length=150), nullable=False),
        sa.Column("road_class", sa.String(length=50), nullable=False),
        sa.Column("speed_limit_kph", sa.Float(), nullable=False),
        sa.Column("length_m", sa.Float(), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("is_forbidden", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("geometry_json", sa.String(length=4000), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["start_node_id"], ["map_nodes.id"]),
        sa.ForeignKeyConstraint(["end_node_id"], ["map_nodes.id"]),
    )
    op.create_index(op.f("ix_map_edges_id"), "map_edges", ["id"], unique=False)
    op.create_index(op.f("ix_map_edges_start_node_id"), "map_edges", ["start_node_id"], unique=False)
    op.create_index(op.f("ix_map_edges_end_node_id"), "map_edges", ["end_node_id"], unique=False)

    op.create_table(
        "hazard_markers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("marker_type", sa.String(length=50), nullable=False),
        sa.Column("severity", sa.Integer(), nullable=False),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("lng", sa.Float(), nullable=False),
        sa.Column("note", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index(op.f("ix_hazard_markers_id"), "hazard_markers", ["id"], unique=False)
    op.create_index(op.f("ix_hazard_markers_user_id"), "hazard_markers", ["user_id"], unique=False)

    op.create_table(
        "manual_routes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("path_json", sa.String(length=8000), nullable=False),
        sa.Column("distance_km", sa.Float(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index(op.f("ix_manual_routes_id"), "manual_routes", ["id"], unique=False)
    op.create_index(op.f("ix_manual_routes_user_id"), "manual_routes", ["user_id"], unique=False)

    op.create_table(
        "runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("distance_km", sa.Float(), nullable=False, server_default="0"),
        sa.Column("duration_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("notes", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index(op.f("ix_runs_id"), "runs", ["id"], unique=False)
    op.create_index(op.f("ix_runs_user_id"), "runs", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_runs_user_id"), table_name="runs")
    op.drop_index(op.f("ix_runs_id"), table_name="runs")
    op.drop_table("runs")

    op.drop_index(op.f("ix_manual_routes_user_id"), table_name="manual_routes")
    op.drop_index(op.f("ix_manual_routes_id"), table_name="manual_routes")
    op.drop_table("manual_routes")

    op.drop_index(op.f("ix_hazard_markers_user_id"), table_name="hazard_markers")
    op.drop_index(op.f("ix_hazard_markers_id"), table_name="hazard_markers")
    op.drop_table("hazard_markers")

    op.drop_index(op.f("ix_map_edges_end_node_id"), table_name="map_edges")
    op.drop_index(op.f("ix_map_edges_start_node_id"), table_name="map_edges")
    op.drop_index(op.f("ix_map_edges_id"), table_name="map_edges")
    op.drop_table("map_edges")

    op.drop_index(op.f("ix_map_nodes_id"), table_name="map_nodes")
    op.drop_table("map_nodes")
