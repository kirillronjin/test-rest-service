import sqlalchemy
from sqlalchemy import Column, DateTime, ForeignKey, String, text, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID

metadata = sqlalchemy.MetaData()

category = sqlalchemy.Table(
    "category",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("code", String, unique=True),
    Column("name", String),
    Column("description", Text),
    Column("parent_category_id", UUID(as_uuid=True), ForeignKey("category.id"), nullable=True),
    Column("is_hidden", Boolean),
    Column("creation_date", DateTime(timezone=True), server_default=text("timezone('utc', now())"), nullable=False),
    Column("modification_date", DateTime(timezone=True), server_default=text("timezone('utc', now())"), nullable=False),
)

category_model = sqlalchemy.Table(
    "category_model",
    metadata,
    Column("category_id", UUID(as_uuid=True), ForeignKey("category.id"), primary_key=True),
    Column("model_id", UUID(as_uuid=True), ForeignKey("product_model.id"), primary_key=True),
)

product_model = sqlalchemy.Table(
    "product_model",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("code", String, unique=True),
    Column("name", String),
    Column("description", Text),
    Column("creation_date", DateTime(timezone=True), server_default=text("timezone('utc', now())"), nullable=False),
    Column("modification_date", DateTime(timezone=True), server_default=text("timezone('utc', now())"), nullable=False),
)
