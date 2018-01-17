"""empty message

Revision ID: 31aaae04a890
Revises: 526dd67fe13a
Create Date: 2018-01-12 08:29:44.166241

"""

# revision identifiers, used by Alembic.
revision = '31aaae04a890'
down_revision = '526dd67fe13a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    sql = """
    CREATE SEQUENCE groups_id_seq;
    CREATE TABLE groups
    (
    id integer NOT NULL DEFAULT nextval('groups_id_seq'::regclass),
    name character varying(100)
    );

    ALTER TABLE public.equipment ADD COLUMN group_id integer;
    ALTER TABLE public.campaign ADD COLUMN group_id integer;
    ALTER TABLE public.contract ADD COLUMN group_id integer;
    ALTER TABLE public.users_user ADD COLUMN group_id integer;
    ALTER TABLE public.location ADD COLUMN group_id integer;

    insert into groups  (id, name) values(1, 'main group');
    UPDATE equipment SET  group_id = 1;
    UPDATE campaign SET  group_id = 1;
    UPDATE contract SET  group_id = 1;
    UPDATE users_user SET  group_id = 1;
    UPDATE location SET  group_id = 1;

    insert into role (id, name, description) values (8, 'group_admin', 'group admin');
    insert into role (id, name, description) values (9, 'group_user', 'group user');

    """
    op.execute(sql=sql)
    pass


def downgrade():
    sql = """
    DROP TABLE groups;
    ALTER TABLE equipment DROP IF EXISTS group_id;
    ALTER TABLE campaign DROP IF EXISTS group_id;
    ALTER TABLE contract DROP IF EXISTS group_id;
    ALTER TABLE users_user DROP IF EXISTS group_id;
    ALTER TABLE location DROP IF EXISTS group_id;
    """
    op.execute(sql=sql)
    pass
