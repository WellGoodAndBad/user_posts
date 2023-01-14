"""empty message

Revision ID: c6cf9d49ba6d
Revises: 
Create Date: 2023-01-14 14:27:56.282166

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c6cf9d49ba6d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', postgresql.UUID(), nullable=False, comment='ID пользователя'),
    sa.Column('login', sa.Unicode(), nullable=True),
    sa.Column('password', sa.Unicode(length=255), nullable=True, comment='Хэш пароля'),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_users_login'), 'users', ['login'], unique=False)
    op.create_table('user_post',
    sa.Column('post_id', postgresql.UUID(), nullable=False),
    sa.Column('user_id', postgresql.UUID(), nullable=False),
    sa.Column('text_post', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('post_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_post')
    op.drop_index(op.f('ix_users_login'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
