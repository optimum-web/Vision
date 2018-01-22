"""empty message

Revision ID: 44ffdd582e97
Revises: 31aaae04a890
Create Date: 2018-01-22 10:04:00.349084

"""

# revision identifiers, used by Alembic.
revision = '44ffdd582e97'
down_revision = '31aaae04a890'

from alembic import op
import sqlalchemy as sa


def upgrade():
    sql ="""
    INSERT INTO public.pages (id, author_id, draft, slug, tag) VALUES (9, 1, 0, 'start-guide', 'wiki');
    INSERT INTO public.pages_translation (id, locale, title, text) VALUES (9, 'en', 'Start guide', '### 1) Create a location
From up menu, access Options -> Locations

Press button "Create" and complete form
<img src="../app/static/img/wiki/1.png" style="padding:5px; border:1px solid #BBB;"/>

### 2) Access Dashboard

### 3) From tree, select your Location, and right click on it. Choose New -> Equipment
<img src="../app/static/img/wiki/2.png" style="padding:5px; border:1px solid #BBB;"/>

### 4) Follow the steps from wizzard

### 5) Create a new campaign
From up menu, access Campaigns -> New Campaign  

Follow the wizzard
<img src="../app/static/img/wiki/3.png" style="padding:5px; border:1px solid #BBB;"/>

');
    """
    op.execute(sql=sql)
    pass


def downgrade():
    sql ="""
    delete from pages where id = 9;
    delete from pages_translation where id = 9;

    """
    op.execute(sql=sql)
    pass
