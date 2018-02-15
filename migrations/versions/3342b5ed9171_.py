"""empty message

Revision ID: 3342b5ed9171
Revises: 44ffdd582e97
Create Date: 2018-02-15 14:15:21.910456

"""

# revision identifiers, used by Alembic.
revision = '3342b5ed9171'
down_revision = '44ffdd582e97'

from alembic import op
import sqlalchemy as sa


def upgrade():
    sql =""" 
    ALTER TABLE public.transformer  ALTER COLUMN winding_metal1 TYPE character varying(20);
    ALTER TABLE public.transformer  ALTER COLUMN winding_metal2 TYPE character varying(20);
    """
    op.execute(sql)
    pass


def downgrade():
    sql =""" 
    ALTER TABLE public.transformer  ALTER COLUMN winding_metal1 TYPE integer;
    ALTER TABLE public.transformer  ALTER COLUMN winding_metal2 TYPE integer;
    """
    op.execute(sql)
    pass
