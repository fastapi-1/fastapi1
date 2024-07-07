from pydantic import BaseModel


# STUDENT
class Student_set(BaseModel):
    stid: str  # شماره دانشجویی
    fname: str  # نام
    lname: str  # نام خانوادگی
    father: str  # نام پدر


class Student(Student_set):
    stid: str            # شماره دانشجویی
    fname: str           # نام
    lname: str           # نام خانوادگی
    father: str          # نام پدر
    birth: str           # تاریخ تولد
    ids: str             # سریال شناسنامه
    born_city: str       # شهر محل تولد مرکز استان
    address: str         # آدرس
    postalcode: int      # کد پستی
    cphone: str          # تلفن همراه
    hphone: str          # تلفن ثابت
    department: str      # دانشکده
    major: str           # رشته تحصیلی
    married: str         # وضعیت تاهل
    id: int              # کد ملی
    scourse_ids: int     # کد دروس اخذ شده
    lids: int            # کد اساتید




# PROFESSOR
class Professor_set(BaseModel):
    lid: str             # کد استاد
    fname: str           # نام
    lname: str           # نام خانوادگی
    id: int              # کد ملی


class Professor(Professor_set):
    lid: str             # کد استاد
    fname: str           # نام
    lname: str           # نام خانوادگی
    id: int              # کد ملی
    department: str      # دانشکده
    major: str           # رشته تحصیلی
    birth: str           # تاریخ تولد
    born_city: str       # شهر محل تولد مرکز استان
    address: str         # آدرس
    postalcode: int      # کد پستی
    cphone: str          # تلفن همراه
    hphone: str          # تلفن ثابت
    lcourse_ids: str     # کد دروس ارئه شده




# COURSE
class Course(BaseModel):
    cid: str             # کد درس
    cname: str           # نام درس
    department: str      # دانشکده
    credit: int          # تعداد واحد

