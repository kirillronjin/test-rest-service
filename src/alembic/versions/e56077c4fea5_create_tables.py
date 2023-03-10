"""create_tables

Revision ID: e56077c4fea5
Revises:
Create Date: 2022-12-06 09:41:49.039649

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "e56077c4fea5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "organizations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False
        ),
        sa.Column("created_by", sa.String(), nullable=True),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False
        ),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "vehicles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("vehicle_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("icc_id", sa.String(), nullable=True),
        sa.Column("number_plate", sa.String(), nullable=True),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("business_type", sa.String(), nullable=True),
        sa.Column("org_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False
        ),
        sa.Column("created_by", sa.String(), nullable=True),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False
        ),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("vehicles")
    op.drop_table("organizations")
    # ### end Alembic commands ###
