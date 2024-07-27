"""Added get_classes function

Revision ID: c727f483995b
Revises: b4bcb7a86a24
Create Date: 2024-07-27 21:10:40.915334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c727f483995b'
down_revision: Union[str, None] = 'b4bcb7a86a24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION get_classes(
        user_id BIGINT, 
        pc_id INTEGER, 
        page INTEGER, 
        role VARCHAR
    )
    RETURNS TABLE(
        class_id INTEGER, 
        total_count INTEGER, 
        schedule_datetime TIMESTAMP WITH TIME ZONE, 
        user_timezone DOUBLE PRECISION, 
        status TEXT
    )
    LANGUAGE plpgsql
    AS $$
    DECLARE
        course_classes INT;
        tb_offset INT;
        user_timezone DOUBLE PRECISION;
    BEGIN
        -- Check if user exists
        IF NOT EXISTS (SELECT 1 FROM users AS u WHERE u.id = user_id) THEN
            RETURN QUERY SELECT 
                NULL::INT AS class_id,
                NULL::INT AS total_count,
                NULL::TIMESTAMP WITH TIME ZONE AS schedule_datetime,
                NULL::DOUBLE PRECISION AS user_timezone,
                'User does not exist' AS status;
            RETURN;
        END IF;

        -- Determine user time zone based on role
        IF role = 'tutor' THEN
            SELECT u.time_zone INTO user_timezone
            FROM tutor_courses AS tc
            JOIN users AS u ON tc.tutor_id = u.id
            JOIN private_courses AS pc ON tc.id = pc.course_id
            WHERE tc.tutor_id = user_id AND pc.id = pc_id;
        ELSIF role = 'student' THEN
            SELECT u.time_zone INTO user_timezone
            FROM private_courses AS pc
            JOIN users AS u ON pc.student_id = u.id
            WHERE pc.student_id = user_id AND pc.id = pc_id;
        END IF;

        -- Check if user is associated with the private course
        IF user_timezone IS NULL THEN
            RETURN QUERY SELECT 
                NULL::INT AS class_id,
                NULL::INT AS total_count,
                NULL::TIMESTAMP WITH TIME ZONE AS schedule_datetime,
                NULL::DOUBLE PRECISION AS user_timezone,
                'Private course does not exist or user does not belong to it' AS status;
            RETURN;
        END IF;

        -- Get the total number of classes for the private course
        SELECT COUNT(*) INTO course_classes FROM private_classes AS pc WHERE pc.private_course_id = pc_id;

        -- Calculate offset for pagination
        tb_offset := (page - 1) * 3;

        -- Return the paginated classes with status
        RETURN QUERY WITH ReturnTable AS (
            SELECT 
                pc.id, 
                course_classes, 
                pc.schedule_datetime, 
                user_timezone,
                CASE
                    WHEN pc.is_paid THEN 'paid'
                    WHEN pc.has_occurred THEN 'occurred'
                    ELSE 'scheduled'
                END AS status
            FROM private_classes AS pc
            WHERE pc.private_course_id = pc_id
            ORDER BY pc.schedule_datetime
            LIMIT 3 OFFSET tb_offset
        ) 
        SELECT * FROM ReturnTable ORDER BY schedule_datetime DESC;
    END;
    $$;

    ALTER FUNCTION get_classes(BIGINT, INTEGER, INTEGER, VARCHAR) OWNER TO postgres;
    """)


def downgrade() -> None:
    op.execute("""
    DROP FUNCTION IF EXISTS get_classes(
        BIGINT, 
        INTEGER, 
        INTEGER, 
        VARCHAR
    );
    """)


