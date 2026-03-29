"""updated_at

Revision ID: 87cf38d6cf55
Revises: 50d34e3f5130
Create Date: 2026-03-29 17:14:53.208669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87cf38d6cf55'
down_revision: Union[str, None] = '50d34e3f5130'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
