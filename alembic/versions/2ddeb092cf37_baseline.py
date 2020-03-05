"""baseline

Revision ID: 2ddeb092cf37
Revises: 
Create Date: 2020-01-14 14:23:15.613798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ddeb092cf37'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), unique=True, nullable=False),
        sa.Column('passwordhash', sa.String(), nullable=False),
        sa.Column('useremail', sa.String(), nullable=False)
    )


def downgrade():
    op.drop_table('users')
