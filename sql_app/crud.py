# ایجاد ارتباط با پایگاه داده و تعریف عملیات مورد نیاز برای مدیریت دانشجویان، استادان و دروس

# وارد کردن کلاس Session از SQLAlchemy ORM برای مدیریت نشست‌های پایگاه داده
from sqlalchemy.orm import Session
from . import models, schemas  # وارد کردن مدل‌ها و اسکیماها از ماژول فعلی
from fastapi import HTTPException  # وارد کردن استثنائات HTTP از FastAPI



# STUDENT

def create_student(db: Session, student: schemas.Student):
    """
    ایجاد یک دانشجو جدید در پایگاه داده
    :param db: نشست دیتابیس
    :param student: اطلاعات دانشجو برای ثبت
    :return: شی دانشجوی ایجاد شده
    """
    db_student = models.Student(
        stid=student.stid,
        fname=student.fname,
        lname=student.lname,
        father=student.father,
        birth=student.birth,
        ids=student.ids,
        born_city=student.born_city,
        address=student.address,
        postalcode=student.postalcode,
        cphone=student.cphone,
        hphone=student.hphone,
        department=student.department,
        major=student.major,
        married=student.married,
        id=student.id,
        scourse_ids=student.scourse_ids,
        lids=student.lids
    )
    db.add(db_student)  # افزودن دانشجو به نشست
    db.commit()  # ثبت تراکنش در پایگاه داده
    db.refresh(db_student)  # به‌روزرسانی شی دانشجو برای دریافت مقادیر به‌روز شده
    return db_student  # بازگشت شی دانشجو ایجاد شده



def get_student(db: Session, student_stid: str) -> schemas.Student_set:
    """
    دریافت یک دانشجو براساس شماره دانشجویی و بازگرداندن فقط چهار فیلد اول.

    :param db: نشست دیتابیس
    :param student_stid: شماره دانشجویی
    :return: شی دانشجوی با چهار فیلد اول
    """
    db_student = db.query(models.Student).filter(models.Student.stid == student_stid).first()
    if db_student:
        student_set = schemas.Student_set(
            stid=db_student.stid,
            fname=db_student.fname,
            lname=db_student.lname,
            father=db_student.father
        )
        return student_set
    else:
        raise HTTPException(status_code=404, detail="stid not found")

# def get_student(db: Session, student_stid: str) -> models.Student:
#     """
#     دریافت یک دانشجو براساس شماره دانشجویی
#
#     :param db: نشست دیتابیس
#     :param student_stid: شماره دانشجویی
#     :return: شی دانشجوی مطابق با شماره دانشجویی داده شده
#     """
#     return db.query(models.Student).filter(models.Student.stid == student_stid).first()






def update_student(db: Session, student_stid: str, new_student_data: schemas.Student_set):
    """
    به‌روزرسانی اطلاعات یک دانشجو براساس شماره دانشجویی.

    :param db: نشست دیتابیس
    :param student_stid: شماره دانشجویی
    :param new_student_data: اطلاعات جدید دانشجو برای به‌روزرسانی
    :return: شی دانشجوی به‌روزرسانی شده
    """
    db_student = db.query(models.Student).filter(models.Student.stid == student_stid).first()
    if db_student:
        # به‌روزرسانی هر ویژگی از دانشجو با مقادیر جدید
        for attr, value in vars(new_student_data).items():
            setattr(db_student, attr, value)
        db.commit()  # ثبت تراکنش برای ذخیره تغییرات
        db.refresh(db_student)  # به‌روزرسانی شی دانشجو برای دریافت مقادیر به‌روز شده
        return db_student  # بازگشت شی دانشجوی به‌روزرسانی شده
    else:
        raise HTTPException(status_code=404, detail="stid not found")




def delete_student(db: Session, student_stid: str):
    """
    حذف یک دانشجو براساس شماره دانشجویی

    :param db: نشست دیتابیس
    :param student_stid: شماره دانشجویی
    :return: پاسخ JSON موفقیت‌آمیز در صورت حذف موفقیت‌آمیز
    """
    db_student = db.query(models.Student).filter(models.Student.stid == student_stid).first()
    if db_student:
        db.delete(db_student)  # حذف شیء دانشجو از نشست
        db.commit()  # ثبت تراکنش برای اعمال تغییرات در پایگاه داده
        return db_student
    return None  # اگر دانشجو پیدا نشد، بازگرداندن None


# PROFESSOR

def create_professor(db: Session, professor: schemas.Professor):
    """
    ایجاد یک استاد جدید در پایگاه داده.

    :param db: نشست دیتابیس
    :param professor: اطلاعات استاد برای ثبت
    :return: شیء استاد ایجاد شده
    """
    db_professor = models.Professor(
        lid=professor.lid,
        fname=professor.fname,
        lname=professor.lname,
        id=professor.id,
        department=professor.department,
        major=professor.major,
        birth=professor.birth,
        born_city=professor.born_city,
        address=professor.address,
        postalcode=professor.postalcode,
        cphone=professor.cphone,
        hphone=professor.hphone,
        lcourse_ids=professor.lcourse_ids,
    )
    db.add(db_professor)  # افزودن استاد به نشست
    db.commit()  # ثبت تراکنش در پایگاه داده
    db.refresh(db_professor)  # به‌روزرسانی شیء استاد برای دریافت مقادیر به‌روز شده
    return db_professor  # بازگشت شیء استاد ایجاد شده

def get_professor(db: Session, professor_lid: str) -> schemas.Professor_set:
    """
    دریافت یک استاد براساس کد استادی.

    :param db: نشست دیتابیس
    :param professor_lid: کد استادی
    :return: شیء استاد مطابق با کد استادی داده شده
    """
    db_professor = db.query(models.Professor).filter(models.Professor.lid == professor_lid).first()
    if db_professor:
        professor_set = schemas.Professor_set(
            lid=db_professor.lid,
            fname=db_professor.fname,
            lname=db_professor.lname,
            id=db_professor.id
        )
        return professor_set
    else:
        raise HTTPException(status_code=404, detail="lid not found")





def update_professor(db: Session, professor_lid: str, new_professor_data: schemas.Professor_set):
    """
    به روزرسانی اطلاعات یک استاد براساس کد استاد

    :param db: نشست دیتابیس
    :param professor_lid: کد استادی
    :param new_professor_data: اطلاعات جدید استاد برای به روزرسانی
    :return: شی استاد به روزرسانی شده
    """
    db_professor = db.query(models.Professor).filter(models.Professor.lid == professor_lid).first()
    if db_professor:
        # به روزرسانی هر ویژگی از استاد با مقادیر جدید
        for attr, value in vars(new_professor_data).items():
            setattr(db_professor, attr, value)
        db.commit()  # ثبت تراکنش برای ذخیره تغییرات
        db.refresh(db_professor)  # به‌روزرسانی شی استاد برای دریافت مقادیر به‌روز شده
        return db_professor  # بازگشت شی استاد به‌روزرسانی شده
    raise HTTPException(status_code=404, detail="lid not found")




def delete_professor(db: Session, professor_lid: str):
    """
    حذف یک استاد براساس کد استاد

    :param db: نشست دیتابیس
    :param professor_lid: کد استاد
    :return: پاسخ JSON موفقیت آمیز در صورت حذف موفقیت آمیز
    """
    db_professor = db.query(models.Professor).filter(models.Professor.lid == professor_lid).first()
    if db_professor:
        db.delete(db_professor)  # حذف شی استاد از نشست
        db.commit()  # ثبت تراکنش برای اعمال تغییرات در پایگاه داده
        return db_professor # بازگرداندن شی استاد حذف شده
    return None # اگر استاد پیدا نشد، بازگرداندن None




# COURSE

def create_course(db: Session, course: schemas.Course):
    """
    ایجاد یک درس جدید در پایگاه داده

    :param db: نشست دیتابیس
    :param course: اطلاعات درس برای ثبت
    :return: شی درس ایجاد شده
    """
    db_course = models.Course(
        cid=course.cid,
        cname=course.cname,
        department=course.department,
        credit=course.credit
    )
    db.add(db_course)  # افزودن درس به نشست
    db.commit()  # ثبت تراکنش در پایگاه داده
    db.refresh(db_course)  # به‌روزرسانی شی درس برای دریافت مقادیر به‌روز شده
    return db_course  # بازگشت شی درس ایجاد شده


def get_course(db: Session, course_cid: str) -> models.Course:
    """
    دریافت یک درس براساس کد درسی

    :param db: نشست دیتابیس
    :param course_cid: کد درسی
    :return: شی درس مطابق با کد درسی داده شده
    """
    return db.query(models.Course).filter(models.Course.cid == course_cid).first()


def update_course(db: Session, course_cid: str, new_course_data: schemas.Course):
    """
    به‌روزرسانی اطلاعات یک درس براساس کد درس

    :param db: نشست دیتابیس
    :param course_cid: کد درسی
    :param new_course_data: اطلاعات جدید درس برای به روزرسانی
    :return: شی درس به روزرسانی شده
    """
    db_course = db.query(models.Course).filter(models.Course.cid == course_cid).first()
    if db_course:
        # به روزرسانی هر ویژگی از درس با مقادیر جدید
        for attr, value in vars(new_course_data).items():
            setattr(db_course, attr, value)
        db.commit()  # ثبت تراکنش برای ذخیره تغییرات
        db.refresh(db_course)  # به‌روزرسانی شی درس برای دریافت مقادیر به‌روز شده
        return db_course  # بازگشت شی درس به روزرسانی شده
    raise HTTPException(status_code=404, detail="cid not found")


def delete_course(db: Session, course_cid: str):
    """
    حذف یک درس براساس کد درسی

    :param db: نشست دیتابیس
    :param course_cid: کد درسی
    :return: شی درس حذف شده
    """
    db_course = db.query(models.Course).filter(models.Course.cid == course_cid).first()
    if db_course:
        db.delete(db_course)  # حذف شی درس از نشست
        db.commit()  # ثبت تراکنش برای اعمال تغییرات در پایگاه داده
        return db_course  # بازگرداندن شی درس حذف شده
    return None  # اگر درس پیدا نشد، بازگرداندن None

