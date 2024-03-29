"""init

Revision ID: 891640b6839e
Revises: 
Create Date: 2024-03-07 11:14:50.872944

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "891640b6839e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("chats",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("is_personal", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table("skills",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("habr_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("habr_id"),
    )
    op.create_table("specialization_groups",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("habr_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("name_en", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("habr_id"),
    )
    op.create_table("users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(length=72), nullable=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("avatar", sa.String(), nullable=True),
        sa.Column("telegram", sa.String(), nullable=True),
        sa.Column("is_activated", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("avatar"),
        sa.UniqueConstraint("telegram"),
        sa.UniqueConstraint("email"),
    )
    op.create_table("chat_members",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("chat_id", sa.Uuid(), nullable=False),
        sa.Column("leave_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("join_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["chat_id"], ["chats.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table("notifications",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("recipient_id", sa.Uuid(), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["recipient_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table("projects",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("owner_id", sa.Uuid(), nullable=False),
        sa.Column("startline", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("avatar", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("projects__owner_id_idx", "projects", ["owner_id"], unique=False,
                    postgresql_using="hash")
    op.create_table("specializations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("habr_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("name_en", sa.String(), nullable=False),
        sa.Column("group_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["group_id"], ["specialization_groups.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("habr_id"),
    )
    op.create_table("user_skills",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("skill_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("user_id", "skill_id"),
    )
    op.create_table("messages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("chat_id", sa.Uuid(), nullable=False),
        sa.Column("member_id", sa.Uuid(), nullable=False),
        sa.Column("text", sa.String(length=2048), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["chat_id"], ["chats.id"]),
        sa.ForeignKeyConstraint(["member_id"], ["chat_members.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table("positions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("specialization_id", sa.Uuid(), nullable=False),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["specialization_id"], ["specializations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("positions__project_id_idx", "positions", ["project_id"], unique=False,
                    postgresql_using="hash")
    op.create_index("positions__specialization_id_idx", "positions", ["specialization_id"],
                    unique=False, postgresql_using="hash")
    op.create_index("positions__created_at_idx", "positions", ["created_at"],
                    unique=False, postgresql_using="btree")
    op.create_table("profiles",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("about", sa.Text(), nullable=True),
        sa.Column("main_specialization_id", sa.Uuid(), nullable=True),
        sa.Column("secondary_specialization_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["main_specialization_id"], ["specializations.id"]),
        sa.ForeignKeyConstraint(["secondary_specialization_id"], ["specializations.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_table("projects_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.Enum("PREPARATION", "IN_WORK", "FINISHED", name="projectstatusenum"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("projects_history__project_id_idx", "projects_history", ["project_id"],
                    unique=False, postgresql_using="hash")
    op.create_index("projects_history__created_at_idx", "projects_history", ["created_at"],
                    unique=False, postgresql_using="btree")
    op.create_table("reviews",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("from_user_id", sa.Uuid(), nullable=False),
        sa.Column("to_user_id", sa.Uuid(), nullable=False),
        sa.Column("rate", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["from_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["to_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("reviews__from_user_id_idx", "reviews", ["from_user_id"], unique=False,
                    postgresql_using="hash")
    op.create_index("reviews__project_id_idx", "reviews", ["project_id"], unique=False,
                    postgresql_using="hash")
    op.create_index("reviews__to_user_id_idx", "reviews", ["to_user_id"], unique=False,
                    postgresql_using="hash")
    op.create_table("participants",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("position_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.Enum("REQUEST", "DECLINED", "JOINED", "LEFT",
                                    name="participantstatusenum"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["position_id"], ["positions.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("participants__position_id_idx", "participants", ["position_id"], unique=False,
                    postgresql_using="hash")
    op.create_index("participants__user_id_idx", "participants", ["user_id"], unique=False,
                    postgresql_using="hash")
    op.create_table("positions_skills",
        sa.Column("position_id", sa.Uuid(), nullable=False),
        sa.Column("skill_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["position_id"], ["positions.id"]),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"]),
        sa.PrimaryKeyConstraint("position_id", "skill_id"),
    )
    op.create_index("positions_skills__created_at_idx", "positions_skills", ["created_at"],
                    unique=False, postgresql_using="btree")
    op.create_index("positions_skills__position_id_idx", "positions_skills", ["position_id"],
                    unique=False, postgresql_using="hash")
    op.create_index("positions_skills__skill_id_idx", "positions_skills", ["skill_id"],
                    unique=False, postgresql_using="hash")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()

    op.drop_index("positions_skills__skill_id_idx", table_name="positions_skills",
                  postgresql_using="hash")
    op.drop_index("positions_skills__position_id_idx", table_name="positions_skills",
                  postgresql_using="hash")
    op.drop_index("positions_skills__created_at_idx", table_name="positions_skills",
                  postgresql_using="btree")
    op.drop_table("positions_skills")
    op.drop_index("participants__user_id_idx", table_name="participants", postgresql_using="hash")
    op.drop_index("participants__position_id_idx", table_name="participants",
                  postgresql_using="hash")
    op.drop_table("participants")
    if bind.engine.name == "postgresql":
        op.execute("DROP TYPE participantstatusenum")
    op.drop_index("reviews__to_user_id_idx", table_name="reviews", postgresql_using="hash")
    op.drop_index("reviews__project_id_idx", table_name="reviews", postgresql_using="hash")
    op.drop_index("reviews__from_user_id_idx", table_name="reviews", postgresql_using="hash")
    op.drop_table("reviews")
    op.drop_index("projects_history__project_id_idx", table_name="projects_history",
                  postgresql_using="hash")
    op.drop_table("projects_history")
    if bind.engine.name == "postgresql":
        op.execute("DROP TYPE projectstatusenum")
    op.drop_table("profiles")
    op.drop_index("positions__specialization_id_idx", table_name="positions",
                  postgresql_using="hash")
    op.drop_index("positions__project_id_idx", table_name="positions", postgresql_using="hash")
    op.drop_table("positions")
    op.drop_table("messages")
    op.drop_table("user_skills")
    op.drop_table("specializations")
    op.drop_index("projects__owner_id_idx", table_name="projects", postgresql_using="hash")
    op.drop_table("projects")
    op.drop_table("notifications")
    op.drop_table("chat_members")
    op.drop_table("users")
    op.drop_table("specialization_groups")
    op.drop_table("skills")
    op.drop_table("chats")
    # ### end Alembic commands ###
