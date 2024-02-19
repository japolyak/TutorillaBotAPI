from fastapi import status, APIRouter, Depends
from .schemas import NewClassDto
from database.crud import tutor_student_crud
from sqlalchemy.orm import Session
from database.db_setup import get_db


router = APIRouter()


@router.post(path="/private-courses/{course_id}/new-class/", status_code=status.HTTP_201_CREATED,
             description="Add new class for private course")
async def add_new_class(course_id: int, new_class: NewClassDto, db: Session = Depends(get_db)):
    schedule = new_class.date
    assignment = {
        "sources": [source.model_dump_json() for source in new_class.sources]
    }
    db_class = tutor_student_crud.schedule_class(db=db, course_id=course_id, schedule=schedule, assignment=assignment)

    return status.HTTP_201_CREATED
