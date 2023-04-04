"""add station order

Revision ID: 2f6592191291
Revises: 8741480c2ca3
Create Date: 2023-03-29 14:21:01.680642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2f6592191291"
down_revision = "8741480c2ca3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "stationen", sa.Column("order", sa.Integer(), nullable=True)
    )
    op.execute("UPDATE stationen SET \"order\" = 0;")
    op.alter_column("stationen", "order", nullable=False)
    pass


def downgrade() -> None:
    op.drop_column("stationen", "order")
    pass
