


"""init

Revision ID: 4137570d05c6
Revises: 
Create Date: 2023-10-18 23:06:06.699410

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4137570d05c6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Uuid(), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_positions',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('project_id', sa.Uuid(), nullable=False),
    sa.Column('specialization_id', sa.Uuid(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id', 'project_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('projects_history',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('project_id', sa.Uuid(), nullable=False),
    sa.Column('status', sa.Enum('PREPARATION', 'IN_WORK', 'FINISHED', name='projectstatusenum'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id', 'project_id')
    )
    op.create_table('project_participants',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('position_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('status', sa.Enum('REQUEST', 'DECLINED', 'JOINED', 'LEFT', name='participantstatusenum'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('joined_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['position_id'], ['project_positions.id'], ),
    sa.PrimaryKeyConstraint('id', 'position_id')
    )
    op.create_table('project_positions_skills',
    sa.Column('position_id', sa.Uuid(), nullable=False),
    sa.Column('skill_id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['position_id'], ['project_positions.id'], ),
    sa.PrimaryKeyConstraint('position_id', 'skill_id')
    )
    ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_participants')
    op.drop_table('projects_history')
    op.drop_table('project_positions')
    op.drop_table('projects')
    op.drop_table('project_positions_skills')
    # ### end Alembic commands ###
