"""Initial migration

Revision ID: 8685f124ac4f
Revises: 
Create Date: 2023-09-26 15:16:41.539644

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sapphire.projects.database.models import (
    ParticipantStatusEnum, ProjectStatusEnum
)

# revision identifiers, used by Alembic.
revision: str = '8685f124ac4f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### adjusted ###
    op.create_table('projects',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('owner_id', sa.UUID(), nullable=False),
                    sa.Column('deadline', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_positions',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('project_id', sa.UUID(), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects_history',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('project_id', sa.UUID(), nullable=True),
                    sa.Column('status', ProjectStatusEnum(name='ProjectStatusEnum'), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('project_participants',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('position_id', sa.UUID(), nullable=True),
                    sa.Column('user_id', sa.UUID(), nullable=True),
                    sa.Column('status', ParticipantStatusEnum(name='ParticipantStatusEnum'), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['position_id'], ['project_positions.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### adjusted ###
    op.drop_table('project_participants')
    op.drop_table('projects_history')
    op.drop_table('project_positions')
    op.drop_table('projects')
    # ### end Alembic commands ###
