"""Initial migration

Revision ID: 6d307b5125b4
Revises: 
Create Date: 2023-09-27 17:03:00.716617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d307b5125b4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### adjusted ###
    op.create_table('projects',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Uuid(), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_positions',
    sa.Column('id', sa.Uuid(), nullable=False, unique=True),
    sa.Column('project_id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id', 'project_id')
    )
    op.create_table('projects_history',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('project_id', sa.Uuid(), nullable=False),
    sa.Column('status', sa.Enum('activated', 'deactivated', name='ProjectStatusEnum', create_constraint=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id', 'project_id')
    )
    op.create_table('project_participants',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('position_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('status', sa.Enum('active', 'inactive', name='ParticipantStatusEnum', create_constraint=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['position_id'], ['project_positions.id'], ),
    sa.PrimaryKeyConstraint('id', 'position_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### adjusted ###
    op.drop_table('project_participants')
    op.drop_table('projects_history')
    op.drop_table('project_positions')
    op.drop_table('projects')
    # ### end Alembic commands ###
