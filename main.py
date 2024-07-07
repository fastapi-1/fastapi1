# from typing import List
# وارد کردن متغیرهای لازم از FastAPI و SQLAlchemy ORM
from fastapi import Depends, FastAPI, HTTPException

# وارد کردن کلاس Session از SQLAlchemy ORM برای استفاده در توابع CRUD
from sqlalchemy.orm import Session

# وارد کردن کلاس‌ها و توابع CRUD از بخشهای مختلف پروژه
from . import crud, models, schemas

# وارد کردن اتصال موقت به دیتابیس و مهیا کردن متغیرهای مربوطه
from .database import SessionLocal, engine

# وارد کردن توابع اعتبارسنجی اطلاعات برای دوره، استاد و دانشجو
from .datavalidation import course_datavalidation, professor_datavalidation, student_datavalidation

from fastapi.responses import JSONResponse  # وارد کردن پاسخ JSON از FastAPI




# ایجاد جدول‌های دیتابیس اس‌کیو‌ال بر اساس مدل‌های تعریف شده
models.Base.metadata.create_all(bind=engine)

# ایجاد اپلیکیشن FastAPI
app = FastAPI()

# تابع برای تأمین اتصال به دیتابیس به‌صورت موقت و بستن آن پس از استفاده
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# STUDENT

@app.post("/create_student/", response_model=schemas.Student_set)
def create_student(student: schemas.Student, db: Session = Depends(get_db)):
    # اعتبارسنجی‌های مختلف برای ایجاد دانشجو
    student_datavalidation.student_exists_check(db, student.stid)
    student_datavalidation.check_stid(db, student.stid)
    student_datavalidation.check_fflname(db, student.fname, student.lname, student.father)
    student_datavalidation.check_birth(db, student.birth)
    student_datavalidation.check_ids(db, student.ids)
    student_datavalidation.born_city(db, student.born_city)
    student_datavalidation.check_address(db, student.address)
    student_datavalidation.check_postalcode(db, student.postalcode)
    student_datavalidation.check_cphone(db, student.cphone)
    student_datavalidation.check_hphone(db, student.hphone)
    student_datavalidation.check_department(db, student.department)
    student_datavalidation.check_major(db, student.major)
    student_datavalidation.check_married(db, student.married)
    student_datavalidation.check_id(db, student.id)

    # ایجاد دانشجو با استفاده از دیتابیس
    return crud.create_student(db=db, student=student)

@app.get("/get_student/{student_stid}", response_model=schemas.Student_set)
def read_student(student_stid: str, db: Session = Depends(get_db)):
    # خواندن اطلاعات دانشجو بر اساس شماره دانشجویی
    db_student = crud.get_student(db, student_stid=student_stid)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student



@app.put("/update_student/{student_stid}", response_model=schemas.Student_set)
def update_student(student_stid: str, new_data: schemas.Student, db: Session = Depends(get_db)):
    # اعتبارسنجی‌های مختلف برای به‌روزرسانی اطلاعات دانشجو
    student_datavalidation.check_stid(db, new_data.stid)
    student_datavalidation.check_fflname(db, new_data.fname, new_data.lname, new_data.father)
    student_datavalidation.check_birth(db, new_data.birth)
    student_datavalidation.check_ids(db, new_data.ids)
    student_datavalidation.born_city(db, new_data.born_city)
    student_datavalidation.check_address(db, new_data.address)
    student_datavalidation.check_postalcode(db, new_data.postalcode)
    student_datavalidation.check_cphone(db, new_data.cphone)
    student_datavalidation.check_hphone(db, new_data.hphone)
    student_datavalidation.check_department(db, new_data.department)
    student_datavalidation.check_major(db, new_data.major)
    student_datavalidation.check_married(db, new_data.married)
    student_datavalidation.check_id(db, new_data.id)

    # به‌روزرسانی اطلاعات دانشجو در دیتابیس
    db_student = crud.update_student(db, student_stid=student_stid, new_student_data=new_data)
    return db_student



@app.delete("/delete_student/{student_stid}")
def delete_student(student_stid: str, db: Session = Depends(get_db)):
    # حذف دانشجو بر اساس شماره دانشجویی
    deleted_student = crud.delete_student(db, student_stid=student_stid)
    if deleted_student:
        return {"message": "Delete successful"}
        # اگر دانشجو یافت نشد، خطای مناسب با کد 404 بازگردانده می‌شود
    raise HTTPException(status_code=404, detail="Student not found")




# PROFESSOR

@app.post("/create_professor/", response_model=schemas.Professor_set)
def create_professor(professor: schemas.Professor, db: Session = Depends(get_db)):
    # اعتبارسنجی‌های مختلف برای ایجاد استاد
    professor_datavalidation.professor_exists_check(db, professor.lid)
    professor_datavalidation.check_lid(db, professor.lid)
    professor_datavalidation.check_flname(db, professor.fname, professor.lname)
    professor_datavalidation.check_id(db, professor.id)
    professor_datavalidation.check_department(db, professor.department)
    professor_datavalidation.check_major(db, professor.major)
    professor_datavalidation.check_birth(db, professor.birth)
    professor_datavalidation.born_city(db, professor.born_city)
    professor_datavalidation.check_address(db, professor.address)
    professor_datavalidation.check_postalcode(db, professor.postalcode)
    professor_datavalidation.check_cphone(db, professor.cphone)
    professor_datavalidation.check_hphone(db, professor.hphone)

    # ایجاد استاد با استفاده از دیتابیس
    return crud.create_professor(db=db, professor=professor)


@app.get("/get_professor/{professor_lid}", response_model=schemas.Professor_set)
def read_professor(professor_lid: str, db: Session = Depends(get_db)):
    # خواندن اطلاعات استاد بر اساس شناسه
    db_professor = crud.get_professor(db, professor_lid=professor_lid)
    if db_professor is None:
        # اگر استاد یافت نشد، خطای مناسب با کد 404 بازگردانده می‌شود
        raise HTTPException(status_code=404, detail="Professor not found")
    return db_professor



@app.put("/update_professor/{professor_lid}", response_model=schemas.Professor_set)
def update_professor(professor_lid: str, new_data: schemas.Professor, db: Session = Depends(get_db)):
    # اعتبارسنجی‌های مختلف برای به‌روزرسانی اطلاعات استاد
    professor_datavalidation.check_lid(db, new_data.lid)
    professor_datavalidation.check_flname(db, new_data.fname, new_data.lname)
    professor_datavalidation.check_id(db, new_data.id)
    professor_datavalidation.check_department(db, new_data.department)
    professor_datavalidation.check_major(db, new_data.major)
    professor_datavalidation.check_birth(db, new_data.birth)
    professor_datavalidation.born_city(db, new_data.born_city)
    professor_datavalidation.check_address(db, new_data.address)
    professor_datavalidation.check_postalcode(db, new_data.postalcode)
    professor_datavalidation.check_cphone(db, new_data.cphone)
    professor_datavalidation.check_hphone(db, new_data.hphone)

    # به‌روزرسانی اطلاعات استاد در دیتابیس
    db_professor = crud.update_professor(db, professor_lid=professor_lid, new_professor_data=new_data)
    return db_professor


@app.delete("/delete_professor/{professor_lid}")
def delete_professor(professor_lid: str, db: Session = Depends(get_db)):
    # حذف استاد بر اساس شناسه
    deleted_professor = crud.delete_professor(db, professor_lid=professor_lid)
    if deleted_professor:
        return {"message": "Delete successful"}
    raise HTTPException(status_code=404, detail="Professor not found")





# COURSE

@app.post("/create_course/", response_model=schemas.Course)
def create_course(course: schemas.Course, db: Session = Depends(get_db)):
    # اعتبارسنجی‌های مختلف برای ایجاد دوره
    course_datavalidation.course_exists_check(db, course.cid)
    course_datavalidation.check_cid(db, course.cid)
    course_datavalidation.check_cname(db, course.cname)
    course_datavalidation.check_department_course(db, course.department)
    course_datavalidation.check_credit(db, course.credit)

    # ایجاد دوره با استفاده از دیتابیس
    return crud.create_course(db=db, course=course)

@app.get("/get_course/{course_cid}", response_model=schemas.Course)
def read_course(course_cid: int, db: Session = Depends(get_db)):
    # خواندن اطلاعات دوره بر اساس شناسه
    db_course = crud.get_course(db, course_cid=course_cid)
    if db_course is None:
        # اگر دوره یافت نشد، خطای مناسب با کد 404 بازگردانده می‌شود
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@app.put("/update_course/{course_cid}", response_model=schemas.Course)
def update_course(course_cid: int, new_data: schemas.Course, db: Session = Depends(get_db)):
    # اعتبارسنجی‌های مختلف برای به‌روزرسانی اطلاعات دوره
    course_datavalidation.check_cid(db, new_data.cid)
    course_datavalidation.check_cname(db, new_data.cname)
    course_datavalidation.check_department_course(db, new_data.department)
    course_datavalidation.check_credit(db, new_data.credit)

    # به‌روزرسانی اطلاعات دوره در دیتابیس
    db_course = crud.update_course(db, course_cid=course_cid, new_course_data=new_data)
    return db_course



@app.delete("/delete_course/{course_cid}")
def delete_course(course_cid: str, db: Session = Depends(get_db)):
    """
    حذف یک درس بر اساس کد درسی

    :param course_cid: کد درسی
    :param db: نشست دیتابیس
    :return: JSONResponse موفقیت آمیز در صورت حذف موفقیت آمیز
    """
    deleted_course = crud.delete_course(db, course_cid=course_cid)
    if deleted_course:
        return {"message": "Delete successful"}
    raise HTTPException(status_code=404, detail="Course not found")  # اگر دوره یافت نشد، خطای مناسب با کد 404 بازگردانده می‌شود


