"""Add assos table

Revision ID: a34cbf8fc8bc
Revises: 282b44c4ec2b
Create Date: 2024-04-15 11:45:52.083857

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a34cbf8fc8bc'
down_revision: Union[str, None] = '282b44c4ec2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'edges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('node_id', sa.Integer(), nullable=True),
        sa.Column('next_node_id', sa.Integer(), nullable=True),
        sa.Column('yes_or_no', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['next_node_id'], ['nodes.node_id']),
        sa.ForeignKeyConstraint(['node_id'], ['nodes.node_id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'workflows',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'start_nodes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('node_type', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'message_nodes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('node_type', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=255), nullable=True),
        sa.Column('message', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'condition_nodes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('node_type', sa.String(length=20), nullable=False),
        sa.Column('condition', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'end_nodes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('node_type', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'workflow_node_association',
        sa.Column('workflow_id', sa.Integer(), sa.ForeignKey('workflows.id')),
        sa.Column('node_id', sa.Integer(), sa.ForeignKey('nodes.node_id'))
    )


def downgrade() -> None:
    op.drop_table('workflow_node_association')
    op.drop_table('end_nodes')
    op.drop_table('condition_nodes')
    op.drop_table('message_nodes')
    op.drop_table('start_nodes')
    op.drop_table('workflows')
    op.drop_table('edges')
