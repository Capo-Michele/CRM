"""deal status enum

Revision ID: 346ac77d8eac
Revises: 829aab6c4184
Create Date: 2026-06-06 13:55:52.531631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '346ac77d8eac'
down_revision: Union[str, Sequence[str], None] = '829aab6c4184'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    dealstatus = sa.Enum(
        'NEW',
        'QUALIFIED',
        'PROPOSAL',
        'NEGOTIATION',
        'WON',
        'LOST',
        name='dealstatus'
    )

    dealstatus.create(op.get_bind())

    op.alter_column(
        'deals',
        'status',
        existing_type=sa.VARCHAR(length=50),
        type_=dealstatus,
        existing_nullable=False,
        postgresql_using="status::dealstatus"
    )


def downgrade() -> None:
    op.alter_column(
        'deals',
        'status',
        existing_type=sa.Enum(
            'NEW',
            'QUALIFIED',
            'PROPOSAL',
            'NEGOTIATION',
            'WON',
            'LOST',
            name='dealstatus'
        ),
        type_=sa.VARCHAR(length=50),
        existing_nullable=False
    )

    sa.Enum(
        'NEW',
        'QUALIFIED',
        'PROPOSAL',
        'NEGOTIATION',
        'WON',
        'LOST',
        name='dealstatus'
    ).drop(op.get_bind())