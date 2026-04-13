"""updated_at

Revision ID: 861d3bc25194
Revises: e2d34087ff04
Create Date: 2026-03-28 18:17:49.164093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '861d3bc25194'
down_revision: Union[str, None] = 'e2d34087ff04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
