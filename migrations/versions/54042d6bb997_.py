"""empty message

Revision ID: 54042d6bb997
Revises: 
Create Date: 2022-04-13 11:16:11.129340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54042d6bb997'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feeds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('feed_generated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_created', sa.DateTime(), nullable=False),
    sa.Column('username', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('hashed_password', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entry_created', sa.DateTime(), nullable=False),
    sa.Column('source_url', sa.String(length=240), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('published_date', sa.DateTime(), nullable=True),
    sa.Column('authors', sa.String(length=240), nullable=True),
    sa.Column('top_image', sa.String(length=240), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('audio_file', sa.String(length=240), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('feed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['feed_id'], ['feeds.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('articles')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    op.drop_table('feeds')
    # ### end Alembic commands ###
