"""empty message

Revision ID: a246888d078
Revises: 23b944f86423
Create Date: 2018-04-06 07:58:25.973690

"""

# revision identifiers, used by Alembic.
revision = 'a246888d078'
down_revision = '23b944f86423'

from alembic import op
import sqlalchemy as sa


def upgrade():
    sql = """
    ALTER TABLE public.transformer ALTER COLUMN primary_winding_connection TYPE character varying(30);
    ALTER TABLE public.transformer ALTER COLUMN secondary_winding_connection TYPE character varying(30);
    ALTER TABLE public.transformer ALTER COLUMN tertiary_winding_connection TYPE character varying(30);
    ALTER TABLE public.transformer ALTER COLUMN quaternary_winding_connection TYPE character varying(30);
    """

    op.execute(sql)
    pass


def downgrade():
    pass
