"""empty message

Revision ID: 7d9a2d7483d3
Revises: 
Create Date: 2018-11-02 16:33:20.726321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d9a2d7483d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('first_name', sa.String(length=10), nullable=False),
    sa.Column('last_name', sa.String(length=10), nullable=False),
    sa.Column('email', sa.String(length=35), nullable=False),
    sa.Column('picture', sa.String(length=300), nullable=False),
    sa.Column('user_type', sa.String(length=33), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_name', sa.String(length=20), nullable=False),
    sa.Column('image', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=False),
    sa.Column('course_major', sa.String(length=60), nullable=False),
    sa.Column('course_accessibility', sa.String(length=20), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('episode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('episode_name', sa.String(length=30), nullable=False),
    sa.Column('image', sa.String(length=20), nullable=True),
    sa.Column('video', sa.String(length=200), nullable=True),
    sa.Column('text', sa.String(length=3000), nullable=True),
    sa.Column('description', sa.String(length=90), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_course_many_to_many',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_course_many_to_many')
    op.drop_table('episode')
    op.drop_table('course')
    op.drop_table('user')
    # ### end Alembic commands ###
