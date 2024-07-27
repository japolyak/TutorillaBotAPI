"""Added schedule_class_and_get_course procedure

Revision ID: dbf112252fe9
Revises: 751dd2f0159d
Create Date: 2024-07-27 21:53:19.082410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbf112252fe9'
down_revision: Union[str, None] = '751dd2f0159d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE PROCEDURE schedule_class_and_get_course(
        IN pc_id INTEGER, 
        IN sender_role VARCHAR, 
        IN sc_schedule_datetime TIMESTAMP WITH TIME ZONE, 
        IN sc_assignment JSONB, 
        OUT recipient_id BIGINT, 
        OUT recipient_timezone DOUBLE PRECISION, 
        OUT sender_name VARCHAR, 
        OUT subject_name VARCHAR, 
        OUT error VARCHAR
    )
    LANGUAGE plpgsql
    AS $$
    BEGIN
        error = NULL;

        -- Check if the private course exists
        IF NOT EXISTS(SELECT 1 FROM private_courses AS pc WHERE pc.id = pc_id) THEN
            error = 'Private course not found';
            RETURN;
        END IF;

        -- Insert the scheduled class
        INSERT INTO private_classes (private_course_id, schedule_datetime, assignment)
        VALUES (pc_id, sc_schedule_datetime, sc_assignment);

        -- Fetch recipient and sender details based on the role
        IF sender_role = 'student' THEN
            SELECT 
                tu.id, 
                tu.time_zone, 
                st.first_name, 
                s.name
            INTO 
                recipient_id, 
                recipient_timezone, 
                sender_name, 
                subject_name
            FROM 
                private_courses AS pco
            JOIN 
                users AS st ON st.id = pco.student_id
            JOIN 
                tutor_courses AS tc ON tc.id = pco.course_id
            JOIN 
                subjects AS s ON s.id = tc.subject_id
            JOIN 
                users AS tu ON tu.id = tc.tutor_id
            WHERE 
                pco.id = pc_id;
            RETURN;
        END IF;

        -- Fetch recipient and sender details for tutors
        SELECT 
            st.id, 
            st.time_zone, 
            tu.first_name, 
            s.name
        INTO 
            recipient_id, 
            recipient_timezone, 
            sender_name, 
            subject_name
        FROM 
            private_courses AS pco
        JOIN 
            users AS st ON st.id = pco.student_id
        JOIN 
            tutor_courses AS tc ON tc.id = pco.course_id
        JOIN 
            subjects AS s ON s.id = tc.subject_id
        JOIN 
            users AS tu ON tu.id = tc.tutor_id
        WHERE 
            pco.id = pc_id;
        RETURN;
    END
    $$;

    ALTER PROCEDURE schedule_class_and_get_course(
        INTEGER, 
        VARCHAR, 
        TIMESTAMP WITH TIME ZONE, 
        JSONB, 
        OUT BIGINT, 
        OUT DOUBLE PRECISION, 
        OUT VARCHAR, 
        OUT VARCHAR, 
        OUT VARCHAR
    ) OWNER TO postgres;
    """)


def downgrade() -> None:
    op.execute("""
    DROP PROCEDURE IF EXISTS schedule_class_and_get_course(
        INTEGER, 
        VARCHAR, 
        TIMESTAMP WITH TIME ZONE, 
        JSONB, 
        OUT BIGINT, 
        OUT DOUBLE PRECISION, 
        OUT VARCHAR, 
        OUT VARCHAR, 
        OUT VARCHAR
    );
    """)

