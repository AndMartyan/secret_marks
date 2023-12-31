"""initialization

Revision ID: e87addaeaf13
Revises: 
Create Date: 2023-10-10 02:10:07.211067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e87addaeaf13'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('secrets',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('secret_text', sa.LargeBinary(), nullable=False),
    sa.Column('hash', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_secrets_id'), 'secrets', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_secrets_id'), table_name='secrets')
    op.drop_table('secrets')
    # ### end Alembic commands ###
