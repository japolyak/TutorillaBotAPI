"""Added add_user procedure

Revision ID: 2186dbf0afb4
Revises: c727f483995b
Create Date: 2024-07-27 21:34:05.421049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2186dbf0afb4'
down_revision: Union[str, None] = 'c727f483995b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE PROCEDURE add_user(
        IN u_id BIGINT,
        IN u_first_name VARCHAR,
        IN u_last_name VARCHAR,
        IN u_email VARCHAR,
        IN u_normalized_email VARCHAR,
        IN u_time_zone DOUBLE PRECISION,
        IN u_locale VARCHAR,
        OUT error VARCHAR
    )
    LANGUAGE plpgsql
    AS
    $$
    BEGIN
        error = NULL;
    
        IF EXISTS(SELECT 1 FROM users AS u WHERE u.id = u_id) THEN
            error = 'User already exists';
            RETURN;
        END IF;
    
        INSERT
        INTO users (id, first_name, last_name, email, normalized_email, time_zone, locale)
        VALUES (u_id, u_first_name, u_last_name, u_email, u_normalized_email, u_time_zone, u_locale);
    END;
    $$;
    
    ALTER PROCEDURE add_user(
        BIGINT,
        VARCHAR,
        VARCHAR,
        VARCHAR,
        VARCHAR,
        DOUBLE PRECISION,
        VARCHAR,
        OUT VARCHAR
    )
    OWNER TO postgres;
    """)


def downgrade() -> None:
    op.execute("""
        DROP PROCEDURE IF EXISTS add_user(
            BIGINT,
            VARCHAR,
            VARCHAR,
            VARCHAR,
            VARCHAR,
            DOUBLE PRECISION,
            VARCHAR,
            OUT VARCHAR
        );
    """)
