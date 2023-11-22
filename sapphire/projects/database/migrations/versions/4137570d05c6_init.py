"""init

Revision ID: 4137570d05c6
Revises: 
Create Date: 2023-10-18 23:06:06.699410

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4137570d05c6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("projects",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("owner_id", sa.Uuid(), nullable=False),
        sa.Column("startline", sa.DateTime(), nullable=False),
        sa.Column("deadline", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("avatar", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("projects__owner_id_idx", "projects", ["owner_id"], unique=False,
                    postgresql_using="hash")
    op.create_table("positions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("specialization_id", sa.Uuid(), nullable=False),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("positions__project_id_idx", "positions", ["project_id"], unique=False,
                    postgresql_using="hash")
    op.create_index("positions__specialization_id_idx", "positions", ["specialization_id"],
                    unique=False, postgresql_using="hash")
    op.create_table("projects_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.Enum("PREPARATION", "IN_WORK", "FINISHED", name="projectstatusenum"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("projects_history__project_id_idx", "projects_history", ["project_id"],
                    unique=False, postgresql_using="hash")
    op.create_table("participants",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("position_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.Enum("REQUEST", "DECLINED", "JOINED", "LEFT",
                                    name="participantstatusenum"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("joined_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["position_id"], ["positions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("participants__position_id_idx", "participants", ["position_id"], unique=False,
                    postgresql_using="hash")
    op.create_index("participants__user_id_idx", "participants", ["user_id"], unique=False,
                    postgresql_using="hash")
    op.create_table("positions_skills",
        sa.Column("position_id", sa.Uuid(), nullable=False),
        sa.Column("skill_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["position_id"], ["positions.id"]),
        sa.PrimaryKeyConstraint("position_id", "skill_id"),
    )
    op.create_index("positions_skills__position_id_idx", "positions_skills", ["position_id"],
                    unique=False, postgresql_using="hash")
    op.create_index("positions_skills__skill_id_idx", "positions_skills", ["skill_id"],
                    unique=False, postgresql_using="hash")
    op.create_index("positions_skills__created_at_idx", "positions_skills", ["created_at"],
                    unique=False, postgresql_using="btree")
    op.create_table("reviews",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("from_user_id", sa.Uuid(), nullable=False),
        sa.Column("to_user_id", sa.Uuid(), nullable=False),
        sa.Column("rate", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("reviews__from_user_id_idx", "reviews", ["from_user_id"], unique=False,
                    postgresql_using="hash")
    op.create_index("reviews__project_id_idx", "reviews", ["project_id"], unique=False,
                    postgresql_using="hash")
    op.create_index("reviews__to_user_id_idx", "reviews", ["to_user_id"], unique=False,
                    postgresql_using="hash")
    ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("participants__user_id_idx", table_name="participants", postgresql_using="hash")
    op.drop_index("participants__position_id_idx", table_name="participants",
                  postgresql_using="hash")
    op.drop_table("participants")
    op.drop_index("projects_history__project_id_idx", table_name="projects_history",
                  postgresql_using="hash")
    op.drop_table("projects_history")
    op.drop_index("positions_skills__position_id_idx", table_name="positions_skills",
                  postgresql_using="hash")
    op.drop_index("positions_skills__skill_id_idx", table_name="positions_skills",
                  postgresql_using="hash")
    op.drop_index("positions_skills__created_at_idx", table_name="positions_skills",
                  postgresql_using="btree")
    op.drop_table("positions_skills")
    op.drop_index("positions__specialization_id_idx", table_name="positions",
                  postgresql_using="hash")
    op.drop_index("positions__project_id_idx", table_name="positions", postgresql_using="hash")
    op.drop_table("positions")
    op.drop_index("reviews__to_user_id_idx", table_name="reviews", postgresql_using="hash")
    op.drop_index("reviews__project_id_idx", table_name="reviews", postgresql_using="hash")
    op.drop_index("reviews__from_user_id_idx", table_name="reviews", postgresql_using="hash")
    op.drop_table("reviews")
    op.drop_index("projects__owner_id_idx", table_name="projects", postgresql_using="hash")
    op.drop_table("projects")
    op.execute("DROP TYPE projectstatusenum")
    op.execute("DROP TYPE participantstatusenum")
    # ### end Alembic commands ###
