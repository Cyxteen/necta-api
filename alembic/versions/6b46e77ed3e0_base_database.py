"""base-database

Revision ID: 6b46e77ed3e0
Revises: 
Create Date: 2023-05-23 16:11:27.955715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b46e77ed3e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
        sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
        sa.Column('username',sa.String(), nullable=False),
        sa.Column('email',sa.String(), unique=True, nullable=False),
        sa.Column('password',sa.String(), nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
