"""Added add_user_role_request procedure

Revision ID: 751dd2f0159d
Revises: 2186dbf0afb4
Create Date: 2024-07-27 21:45:13.621462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '751dd2f0159d'
down_revision: Union[str, None] = '2186dbf0afb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE PROCEDURE add_user_role_request(
        IN u_id BIGINT,
        IN u_student BOOLEAN,
        IN u_tutor BOOLEAN,
        IN u_request_datetime TIMESTAMP WITH TIME ZONE,
        OUT error VARCHAR
    )
    LANGUAGE plpgsql
    AS $$
    DECLARE
        us_id BIGINT;
        student BOOLEAN;
        tutor BOOLEAN;
    BEGIN
        error = NULL;

        SELECT u.id, u.is_tutor, u.is_student INTO us_id, tutor, student 
        FROM users AS u 
        WHERE u.id = u_id;

        IF (us_id IS NULL) THEN
            error = 'User does not exist';
            RETURN;
        END IF;

        IF ((u_tutor AND tutor) OR (u_student AND student)) THEN
            error = 'User already has the selected role';
            RETURN;
        END IF;

        IF EXISTS(SELECT 1 FROM users_requests AS ur WHERE ur.user_id = u_id) THEN
            error = 'User already made a role request';
            RETURN;
        END IF;

        INSERT INTO users_requests (user_id, request_datetime, student_role, tutor_role)
        VALUES (u_id, u_request_datetime, u_student, u_tutor);
    END;
    $$;

    ALTER PROCEDURE add_user_role_request(
        BIGINT,
        BOOLEAN,
        BOOLEAN,
        TIMESTAMP WITH TIME ZONE,
        OUT VARCHAR
    )
    OWNER TO postgres;
    """)


def downgrade() -> None:
    op.execute("""
    DROP PROCEDURE IF EXISTS add_user_role_request(
        BIGINT,
        BOOLEAN,
        BOOLEAN,
        TIMESTAMP WITH TIME ZONE,
        OUT VARCHAR
    );
    """)
