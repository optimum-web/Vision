"""empty message

Revision ID: 16ba09ca4d95
Revises: 218da0de0144
Create Date: 2016-12-22 16:04:13.198848

"""

# revision identifiers, used by Alembic.
revision = '16ba09ca4d95'
down_revision = '218da0de0144'

from alembic import op
import sqlalchemy as sa


def upgrade():
    sql = """
        ALTER TABLE "public".particles RENAME TO norm_particles;
        UPDATE "public".norm SET table_name = 'norm_particles' WHERE id = 5;

        CREATE SEQUENCE norm_furan_data_id_seq;
        CREATE TABLE IF NOT EXISTS public.norm_furan_data (
            id INT PRIMARY KEY NOT NULL DEFAULT nextval('norm_furan_data_id_seq'::regclass),
            norm_id INT,
            name CHARACTER VARYING(50),
            c1 DOUBLE PRECISION DEFAULT 0,
            c2 DOUBLE PRECISION DEFAULT 0,
            c3 DOUBLE PRECISION DEFAULT 0,
            c4 DOUBLE PRECISION DEFAULT 0,
            equipment_id INT,
            campaign_id INT,
            CONSTRAINT norm_furan_data_norm_id_fk FOREIGN KEY (norm_id) REFERENCES norm_furan (id),
            CONSTRAINT norm_furan_data_equipment_id_fk FOREIGN KEY (equipment_id) REFERENCES equipment (id),
            CONSTRAINT norm_furan_data_campaign_id_fk FOREIGN KEY (campaign_id) REFERENCES campaign (id)
        );

        CREATE SEQUENCE norm_gas_data_id_seq;
        CREATE TABLE IF NOT EXISTS public.norm_gas_data (
            id INT PRIMARY KEY NOT NULL DEFAULT nextval('norm_gas_data_id_seq'::regclass),
            norm_id INT,
            name CHARACTER VARYING(50),
            condition INT DEFAULT 0,
            h2 DOUBLE PRECISION DEFAULT 0,
            ch4 DOUBLE PRECISION DEFAULT 0,
            c2h2 DOUBLE PRECISION DEFAULT 0,
            c2h4 DOUBLE PRECISION DEFAULT 0,
            c2h6 DOUBLE PRECISION DEFAULT 0,
            co DOUBLE PRECISION DEFAULT 0,
            co2 DOUBLE PRECISION DEFAULT 0,
            tdcg DOUBLE PRECISION DEFAULT 0,
            fluid_level INT DEFAULT 0,
            equipment_id INT,
            campaign_id INT,
            CONSTRAINT norm_gas_data_norm_id_fk FOREIGN KEY (norm_id) REFERENCES norm_gas (id),
            CONSTRAINT norm_gas_data_equipment_id_fk FOREIGN KEY (equipment_id) REFERENCES equipment (id),
            CONSTRAINT norm_gas_data_campaign_id_fk FOREIGN KEY (campaign_id) REFERENCES campaign (id)
        );

        CREATE SEQUENCE norm_isolation_data_id_seq;
        CREATE TABLE IF NOT EXISTS public.norm_isolation_data (
            id INT PRIMARY KEY NOT NULL DEFAULT nextval('norm_isolation_data_id_seq'::regclass),
            norm_id INT,
            c DOUBLE PRECISION DEFAULT 0,
            f DOUBLE PRECISION DEFAULT 0,
            notseal DOUBLE PRECISION DEFAULT 0,
            seal DOUBLE PRECISION DEFAULT 0,
            equipment_id INT,
            campaign_id INT,
            CONSTRAINT norm_isolation_data_norm_id_fk FOREIGN KEY (norm_id) REFERENCES norm_isolation (id),
            CONSTRAINT norm_isolation_data_equipment_id_fk FOREIGN KEY (equipment_id) REFERENCES equipment (id),
            CONSTRAINT norm_isolation_data_campaign_id_fk FOREIGN KEY (campaign_id) REFERENCES campaign (id)
        );

        CREATE SEQUENCE norm_physic_data_id_seq;
        CREATE TABLE IF NOT EXISTS public.norm_physic_data (
            id INT PRIMARY KEY NOT NULL DEFAULT nextval('norm_physic_data_id_seq'::regclass),
            norm_id INT,
            name CHARACTER VARYING(20) NOT NULL,
            acid_min DOUBLE PRECISION,
            acid_max DOUBLE PRECISION,
            ift_min DOUBLE PRECISION,
            ift_max DOUBLE PRECISION,
            d1816_min DOUBLE PRECISION,
            d1816_max DOUBLE PRECISION,
            d877_min DOUBLE PRECISION,
            d877_max DOUBLE PRECISION,
            color_min DOUBLE PRECISION,
            color_max DOUBLE PRECISION,
            density_min DOUBLE PRECISION,
            density_max DOUBLE PRECISION,
            pf20_min DOUBLE PRECISION,
            pf20_max DOUBLE PRECISION,
            water_min DOUBLE PRECISION,
            water_max DOUBLE PRECISION,
            flashpoint_min DOUBLE PRECISION,
            flashpoint_max DOUBLE PRECISION,
            pourpoint_min DOUBLE PRECISION,
            pourpoint_max DOUBLE PRECISION,
            viscosity_min DOUBLE PRECISION,
            viscosity_max DOUBLE PRECISION,
            d1816_2_min DOUBLE PRECISION,
            d1816_2_max DOUBLE PRECISION DEFAULT 0,
            p100_min DOUBLE PRECISION,
            p100_max DOUBLE PRECISION,
            fluid_type_id INT DEFAULT 0,
            cei156_min INT DEFAULT 0,
            cei156_max INT DEFAULT 0,
            equipment_id INT,
            campaign_id INT,
            CONSTRAINT norm_physic_data_norm_id_fk FOREIGN KEY (norm_id) REFERENCES norm_physic (id),
            CONSTRAINT norm_physic_data_equipment_id_fk FOREIGN KEY (equipment_id) REFERENCES equipment (id),
            CONSTRAINT norm_physic_data_campaign_id_fk FOREIGN KEY (campaign_id) REFERENCES campaign (id)
        );

        CREATE SEQUENCE norm_particles_data_id_seq;
        CREATE TABLE IF NOT EXISTS public.norm_particles_data (
            id INT PRIMARY KEY NOT NULL DEFAULT nextval('norm_particles_data_id_seq'::regclass),
            norm_id CHARACTER VARYING(50),
            "2um" DOUBLE PRECISION,
            "5um" DOUBLE PRECISION,
            "10um" DOUBLE PRECISION,
            "15um" DOUBLE PRECISION,
            "25um" DOUBLE PRECISION,
            "50um" DOUBLE PRECISION,
            "100um" DOUBLE PRECISION,
            iso4406_1 DOUBLE PRECISION,
            iso4406_2 DOUBLE PRECISION,
            iso4406_3 DOUBLE PRECISION,
            nas1638 DOUBLE PRECISION,
            equipment_id INT,
            campaign_id INT,
            CONSTRAINT norm_particles_data_norm_id_fk FOREIGN KEY (norm_id) REFERENCES norm_particles (id),
            CONSTRAINT norm_particles_data_equipment_id_fk FOREIGN KEY (equipment_id) REFERENCES equipment (id),
            CONSTRAINT norm_particles_data_campaign_id_fk FOREIGN KEY (campaign_id) REFERENCES campaign (id)
        );
        """
    op.execute(sql=sql)


def downgrade():
    sql = """
        DROP TABLE norm_particles_data;
        DROP TABLE norm_physic_data;
        DROP TABLE norm_isolation_data;
        DROP TABLE norm_gas_data;
        DROP TABLE norm_furan_data;

        DROP SEQUENCE norm_particles_data_id_seq;
        DROP SEQUENCE norm_physic_data_id_seq;
        DROP SEQUENCE norm_isolation_data_id_seq;
        DROP SEQUENCE norm_gas_data_id_seq;
        DROP SEQUENCE norm_furan_data_id_seq;

        UPDATE "public".norm SET table_name = 'particles' WHERE id = 5;
        ALTER TABLE "public".norm_particles RENAME TO particles;
        """
    op.execute(sql=sql)
