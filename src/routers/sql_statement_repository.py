from sqlalchemy import text


class SqlStatementRepository:
    get_classes = text("SELECT * FROM public.get_classes(:p1, :p2, :p3, :p4)")

    add_user = text("CALL add_user(:u_id, :u_first_name, :u_last_name, :u_email, :u_normalized_email, :u_time_zone, :u_locale, :error)")
    add_user_role_request = text("CALL add_user_role_request(:u_id, :u_student, :u_tutor, :u_request_datetime, :error)")
    schedule_class_and_get_course = text("CALL schedule_class_and_get_course(:pc_id, :sender_role, :sc_schedule_datetime, :sc_assignment, :recipient_id, :recipient_timezone, :sender_name, :subject_name, :error)")


sql_statements = SqlStatementRepository()
