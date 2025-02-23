"""add location name and characteristic to locations table

Revision ID: 04fcbee53a8a
Revises: e36356c26061
Create Date: 2025-02-23 11:16:17.848197

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "04fcbee53a8a"
down_revision: Union[str, None] = "e36356c26061"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("locations", sa.Column("location_name", sa.Text(), nullable=False))
    op.add_column("locations", sa.Column("characteristic", sa.Text(), nullable=False))


def downgrade() -> None:
    op.drop_column("locations", "location_name")
    op.drop_column("locations", "characteristic")
