import sqlalchemy
from sqlalchemy import Column, DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID

metadata = sqlalchemy.MetaData()

vehicles = sqlalchemy.Table(
    "vehicles",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("vehicle_id", UUID(as_uuid=True), unique=True),
    Column("icc_id", String),
    Column("number_plate", String),
    Column("type", String),
    Column("name", String),
    Column("business_type", String),
    Column("org_id", UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=text("timezone('utc', now())"), nullable=False),
    Column("created_by", String),
    Column("updated_at", DateTime(timezone=True), server_default=text("timezone('utc', now())"), nullable=False),
    Column("updated_by", String),
)

organizations = sqlalchemy.Table(
    "organizations",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String),
    Column("created_at", DateTime(timezone=True), server_default=text("timezone('utc', now())"), nullable=False),
    Column("created_by", String),
    Column("updated_at", DateTime(timezone=True), server_default=text("timezone('utc', now())"), nullable=False),
    Column("updated_by", String),
)
