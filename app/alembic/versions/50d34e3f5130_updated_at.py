"""updated_at

Revision ID: 50d34e3f5130
Revises: 30631c1d73f0
Create Date: 2026-03-29 17:14:22.943556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50d34e3f5130'
down_revision: Union[str, None] = '30631c1d73f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
