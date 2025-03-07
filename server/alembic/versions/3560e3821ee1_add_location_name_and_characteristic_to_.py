"""add location name and characteristic to locations table

Revision ID: 3560e3821ee1
Revises: e36356c26061
Create Date: 2025-02-23 11:33:00.580169

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3560e3821ee1"
down_revision: Union[str, None] = "e36356c26061"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("locations", sa.Column("location_name", sa.Text(), nullable=False))
    op.add_column("locations", sa.Column("characteristic", sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("locations", "characteristic")
    op.drop_column("locations", "location_name")
    # ### end Alembic commands ###
