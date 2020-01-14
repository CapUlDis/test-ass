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


from alembic import op
import sqlalchemy as sa



def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String()),
        sa.Column('passwordhash', sa.String()),
        sa.Column('useremail', sa.String())
    )


def downgrade():
    op.drop_table('users')
