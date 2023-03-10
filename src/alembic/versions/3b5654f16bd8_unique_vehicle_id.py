"""unique vehicle_id

Revision ID: 3b5654f16bd8
Revises: da0f4bed989c
Create Date: 2022-12-09 04:01:55.555143

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "3b5654f16bd8"
down_revision = "da0f4bed989c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "vehicles", ["vehicle_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "vehicles", type_="unique")
    # ### end Alembic commands ###
