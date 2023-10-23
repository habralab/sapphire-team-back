"""Initial migration

Revision ID: 129f61d28e39
Revises: 
Create Date: 2023-09-29 11:18:55.166058

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "129f61d28e39"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### adjusted ###
    op.create_table("skills",
                    sa.Column("id", sa.Uuid(), nullable=False),
                    sa.Column("name", sa.String(), nullable=True),
                    sa.Column("created_at", sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    )
    op.create_table("specialization_groups",
                    sa.Column("id", sa.Uuid(), nullable=False),
                    sa.Column("name", sa.String(), nullable=True),
                    sa.Column("created_at", sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    )
    op.create_table("specializations",
                    sa.Column("id", sa.Uuid(), nullable=False),
                    sa.Column("name", sa.String(), nullable=True),
                    sa.Column("is_other", sa.Boolean(), nullable=False),
                    sa.Column("group_id", sa.Uuid(), nullable=True),
                    sa.Column("created_at", sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(["group_id"], ["specialization_groups.id"]),
                    sa.PrimaryKeyConstraint("id"),
                    )
    op.create_table("specializations_skills",
                    sa.Column("skill_id", sa.Uuid(), nullable=False),
                    sa.Column("specialization_id", sa.Uuid(), nullable=False),
                    sa.Column("created_at", sa.DateTime(), nullable=False),
                    sa.Column("updated_at", sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(["skill_id"], ["skills.id"]),
                    sa.ForeignKeyConstraint(["specialization_id"], ["specializations.id"]),
                    sa.PrimaryKeyConstraint("skill_id", "specialization_id"),
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### adjusted ###
    op.drop_table("specializations_skills")
    op.drop_table("specializations")
    op.drop_table("specialization_groups")
    op.drop_table("skills")
    # ### end Alembic commands ###
