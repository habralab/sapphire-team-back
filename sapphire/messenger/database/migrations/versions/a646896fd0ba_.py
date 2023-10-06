"""empty message

Revision ID: a646896fd0ba
Revises: 
Create Date: 2023-10-06 20:10:56.017374

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a646896fd0ba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('is_personal', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('chat_members',
                    sa.Column('user_id', sa.Uuid(), nullable=False),
                    sa.Column('chat_id', sa.Uuid(), nullable=False),
                    sa.Column('leave_at', sa.DateTime(), nullable=True),
                    sa.Column('join_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
                    sa.PrimaryKeyConstraint('chat_id')
                    )
    op.create_table('messages',
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.Column('chat_id', sa.Uuid(), nullable=False),
                    sa.Column('text', sa.String(length=2048), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('chat_members')
    op.drop_table('chats')
    # ### end Alembic commands ###
