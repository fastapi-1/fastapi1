# ایمپورت کامپوننت های مورد نیاز از SQLAlchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# ایمپورت Base از ماژول database
# Base از SQLAlchemy برای تعریف پایه‌ای که برای ساخت مدل‌های داده‌ای و جداول در پایگاه داده استفاده می‌شود، وارد می‌شود.
from . database import Base
from sqlalchemy.orm import relationship


# STUDENT
class Student(Base):
    """
    جدول مربوط به اطلاعات دانشجویان
    """
    __tablename__ = "student"
    stid = Column(String, primary_key=True)         # شماره دانشجویی
    fname = Column(String)                          # نام
    lname = Column(String)                          # نام خانوادگی
    father = Column(String)                         # نام پدر
    birth = Column(String)                          # تاریخ تولد
    ids = Column(String)                            # سریال شناسنامه
    born_city = Column(String)                      # شهر محل تولد مرکز استان
    address = Column(String)                        # آدرس
    postalcode = Column(Integer)                    # کد پستی
    cphone = Column(String)                         # تلفن همراه
    hphone = Column(String)                         # تلفن ثابت
    department = Column(String)                     # دانشکده
    major = Column(String)                          # رشته تحصیلی
    married = Column(String)                        # وضعیت تاهل
    id = Column(Integer)                            # کد ملی
    scourse_ids = Column(Integer)                   # کد دروس اخذ شده
    lids = Column(Integer)                          # کد اساتید


# PROFESSOR
class Professor(Base):
    """
    جدول مربوط به اطلاعات اساتید
    """
    __tablename__ = 'professor'
    lid = Column(String, primary_key=True)          # کد استاد
    fname = Column(String)                          # نام
    lname = Column(String)                          # نام خانوادگی
    id = Column(Integer)                            # شماره شناسنامه
    department = Column(String)                     # دانشکده
    major = Column(String)                          # رشته تحصیلی
    birth = Column(String)                          # تاریخ تولد
    born_city = Column(String)                      # شهر محل تولد مرکز استان
    address = Column(String)                        # آدرس
    postalcode = Column(Integer)                    # کد پستی
    cphone = Column(String)                         # تلفن همراه
    hphone = Column(String)                         # تلفن ثابت
    lcourse_ids = Column(String)                    # کد دروس ارائه شده


# COURSE
class Course(Base):
    """
    جدول مربوط به اطلاعات دروس
    """
    __tablename__ = "course"
    cid = Column(String, primary_key=True, index=True)    # کد درس
    cname = Column(String)                                # نام درس
    department = Column(String)                           # دانشکده
    credit = Column(Integer)                              # تعداد واحد


