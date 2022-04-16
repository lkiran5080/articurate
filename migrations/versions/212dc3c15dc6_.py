"""empty message

Revision ID: 212dc3c15dc6
Revises: 54042d6bb997
Create Date: 2022-04-14 12:02:59.689611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '212dc3c15dc6'
down_revision = '54042d6bb997'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entries',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('entry_created', sa.DateTime(), nullable=False),
                    sa.Column('source_url', sa.String(
                        length=240), nullable=True),
                    sa.Column('title', sa.String(length=100), nullable=True),
                    sa.Column('published_date', sa.DateTime(), nullable=True),
                    sa.Column('authors', sa.String(length=240), nullable=True),
                    sa.Column('top_image', sa.String(
                        length=240), nullable=True),
                    sa.Column('content', sa.Text(), nullable=True),
                    sa.Column('summary', sa.Text(), nullable=True),
                    sa.Column('audio_file', sa.String(
                        length=240), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('feed_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['feed_id'], ['feeds.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.drop_table('articles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articles',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('entry_created', sa.DATETIME(), nullable=False),
                    sa.Column('source_url', sa.VARCHAR(
                        length=240), nullable=True),
                    sa.Column('title', sa.VARCHAR(length=100), nullable=True),
                    sa.Column('published_date', sa.DATETIME(), nullable=True),
                    sa.Column('authors', sa.VARCHAR(
                        length=240), nullable=True),
                    sa.Column('top_image', sa.VARCHAR(
                        length=240), nullable=True),
                    sa.Column('content', sa.TEXT(), nullable=True),
                    sa.Column('summary', sa.TEXT(), nullable=True),
                    sa.Column('audio_file', sa.VARCHAR(
                        length=240), nullable=True),
                    sa.Column('user_id', sa.INTEGER(), nullable=True),
                    sa.Column('feed_id', sa.INTEGER(), nullable=True),
                    sa.ForeignKeyConstraint(['feed_id'], ['feeds.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.drop_table('entries')
    # ### end Alembic commands ###
