"""updated_at

Revision ID: 27b8332558fd
Revises: 66d71c71be52
Create Date: 2026-03-29 17:46:30.267033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27b8332558fd'
down_revision: Union[str, None] = '66d71c71be52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
