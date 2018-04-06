"""empty message

Revision ID: 23b944f86423
Revises: 3342b5ed9171
Create Date: 2018-03-15 13:21:44.095805

"""

# revision identifiers, used by Alembic.
revision = '23b944f86423'
down_revision = '3342b5ed9171'

from alembic import op
import sqlalchemy as sa


def upgrade():
    sql = """ 
    ALTER TABLE public.equipment ALTER COLUMN assigned_to_id DROP NOT NULL;
    ALTER TABLE public.transformer ALTER COLUMN winding_metal3 TYPE character varying(20);
    ALTER TABLE public.transformer ALTER COLUMN winding_metal4 TYPE character varying(20);

    ALTER TABLE public.transformer ADD fourth_tension double precision;
    ALTER TABLE public.transformer ADD imp_base3 double precision;
    ALTER TABLE public.transformer ADD imp_base4 double precision;
    ALTER TABLE public.transformer ADD cooling_type character varying(20);
    ALTER TABLE public.transformer ADD cooling_stages INT;
    ALTER TABLE public.transformer ADD conservator_type character varying(30);
    """
    op.execute(sql)
    pass


def downgrade():
    pass
