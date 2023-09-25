"""create account table

Revision ID: c9ee93a6daa6
Revises: 
Create Date: 2023-09-25 16:27:59.002418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9ee93a6daa6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.create_table("users",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True)
    )

    # Create the projects table
    op.create_table("projects",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("owner_id", sa.UUID, nullable=False),
        sa.Column("deadline", sa.DateTime, default=sa.Null()),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )

    # Create the projects_history table
    op.create_table("projects_history",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("project_id", sa.UUID, sa.ForeignKey("projects.id")),
        sa.Column("status", sa.Enum("in_progress", "completed", name='status'), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )

    # Create the project_positions table
    op.create_table("project_positions",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("project_id", sa.UUID, sa.ForeignKey("projects.id")),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )

    # Create the project_participants table
    op.create_table("project_participants",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("position_id", sa.UUID, sa.ForeignKey("project_positions.id")),
        sa.Column("user_id", sa.UUID, sa.ForeignKey("users.id")),
        sa.Column("status", sa.Enum("active", "inactive",name='status'), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )

def downgrade():
    # Drop the projects table
    op.drop_table("projects")

    # Drop the projects_history table
    op.drop_table("projects_history")

    # Drop the project_positions table
    op.drop_table("project_positions")

    # Drop the project_participants table
    op.drop_table("project_participants")