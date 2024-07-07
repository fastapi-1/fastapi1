# وارد کردن کلاس HTTPException از FastAPI برای استفاده در مدیریت خطاها
from fastapi import HTTPException

# وارد کردن کلاس Session از SQLAlchemy ORM برای استفاده در توابع CRUD
from sqlalchemy.orm import Session

# وارد کردن ماژول‌های crud، models و schemas از ماژول فعلی
from . import crud, models, schemas





# STUDENT

class student_datavalidation:
    # بررسی وجود دانشجو با استفاده از شماره دانشجویی
    def student_exists_check(db: Session, stid: str):
        student_stid = db.query(models.Student).filter(models.Student.stid == stid).first()
        if student_stid is not None:
            raise HTTPException(status_code=409, detail="student with this stid already exists")

    # بررسی صحت شماره دانشجویی
    def check_stid(db: Session, stid: str):
        if len(stid) != 11:
            raise HTTPException(status_code=400, detail="Student ID must be 11 digits. The entered number of digits is incorrect.")
        if int(stid[0:3]) > 403 or int(stid[0:3]) < 400:
            raise HTTPException(status_code=400, detail="Incorrect year part.")
        if int(stid[3:9]) != 114150:
            raise HTTPException(status_code=400, detail="Incorrect fixed part.")
        if int(stid[9:11]) == 0:
            raise HTTPException(status_code=400, detail="Incorrect index part.")

    # بررسی صحت نام و نام خانوادگی و نام پدر
    def check_fflname(db: Session, fname: str, lname: str, father: str):
        if len(fname) > 10 or len(lname) > 10 or len(father) > 10:
            raise HTTPException(status_code=400, detail="The number of names cannot be more than 10")

        if not all('آ' <= char <= 'ی' or char == ' ' for char in (fname + lname + father)):
            raise HTTPException(status_code=400,
                                detail="The entered name should only contain Persian letters and"
                                       " should not contain numbers, special characters")

    # بررسی صحت تاریخ تولد
    def check_birth(db: Session, birth: str):
        if len(birth) != 10:
            raise HTTPException(status_code=400, detail="The entered date must be exactly 10 digits"
                                                        " and separated by periods")

        parts = birth.split('.')
        if len(parts) != 3:
            raise HTTPException(status_code=400, detail="The date must have three parts"
                                                        " (year, month and day) respectively.")

        year, month, day = parts
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            raise HTTPException(status_code=400, detail="The date entered must contain numbers")

        year = int(year)
        month = int(month)
        day = int(day)

        if not (1300 <= year <= 1402):
            raise HTTPException(status_code=400, detail="The entered year must be between 1300 and 1402")

        if not (1 <= month <= 12):
            raise HTTPException(status_code=400, detail="The month entered must be between 1 and 12")

        if (1 <= month <= 6) and not (1 <= day <= 31):
            raise HTTPException(status_code=400, detail="The day entered must be between 1 and 31")

        if (7 <= month <= 12) and not (1 <= day <= 30):
            raise HTTPException(status_code=400, detail="The day entered must be between 1 and 30")

    # بررسی صحت شماره شناسنامه
    def check_ids(db: Session, ids: str):
        parts = ids.split('.')
        if len(parts) != 3:
            raise HTTPException(status_code=400, detail="Birth certificate serial number must consist of three parts")

        first = parts[0]
        second = parts[1]
        third = parts[2]

        if len(first) != 1:
            raise HTTPException(status_code=400, detail="The first part of the birth certificate serial number must consist of one letter")
        if not ('آ' <= first <= 'ی'):
            raise HTTPException(status_code=400, detail="The first part of the birth certificate serial number must be one of the Persian alphabet letters")

        if len(second) != 2:
            raise HTTPException(status_code=400, detail="The second part of the birth certificate serial number must consist of 2 digits")
        if not second.isdigit():
            raise HTTPException(status_code=400, detail="The second part of the birth certificate serial number must be numeric")
        if len(third) != 6:
            raise HTTPException(status_code=400, detail="The third part of the birth certificate serial number must consist of 6 digits")
        if not third.isdigit():
            raise HTTPException(status_code=400, detail="The third part of the birth certificate serial number must be numeric")

    # بررسی صحت شهر محل تولد مرکز استان
    def born_city(db: Session, born_city: str):
        markaz = ["اراک", "خرم آباد", "تهران", "اردبیل", "تبریز", "اصفهان", "اهواز", "ایلام", "بجنورد", "بیرجند", "مشهد",
                  "بندرعباس", "بوشهر", "ارومیه", "رشت", "زاهدان", "زنجان", "سمنان", "سنندج", "شیراز", "شهرکرد", "قزوین",
                  "قم", "کرج", "کرمان", "کرمانشاه", "گرگان", "همدان", "یاسوج", "یزد"]
        if not (born_city in markaz):
            raise HTTPException(status_code=400, detail="The entered province is not in the list of Iranian provinces"
                                                        " or the input was entered incorrectly")

    # بررسی صحت آدرس
    def check_address(db: Session, address: str):
        if len(address) > 100:
            raise HTTPException(status_code=400, detail="The length of the address exceeds the limit (100 characters).")

    # بررسی صحت کد پستی
    def check_postalcode(db: Session, postalcode: int):
        strpostalcode = str(postalcode)
        if len(strpostalcode) != 10 or not strpostalcode.isdigit():
            raise HTTPException(status_code=400, detail="postalcode must be 10 digits")

    # بررسی صحت تلفن همراه
    def check_cphone(db: Session, cphone: str):
        if len(cphone) != 14 or not cphone[5:].isdigit():
            raise HTTPException(status_code=400, detail="The cphone number entered is not valid")
        if cphone[0:4] != "+98-":
            raise HTTPException(status_code=400, detail="The cphone number must start with +98")

    # بررسی صحت تلفن ثابت
    def check_hphone(db: Session, hphone: str):
        if hphone.count('_') != 1:
            raise HTTPException(status_code=400, detail="The entered hphone number must have two parts prefix"
                                                        " and fixed number and separated by _")

        parts = hphone.split('_')
        first = parts[0]
        second = parts[1]

        if len(first) != 3 or len(second) != 8:
            raise HTTPException(status_code=400, detail="The prefix must be three digits and"
                                                        " the hphone number must be eight digits")

        if not (first.isdigit() and second.isdigit()):
            raise HTTPException(status_code=400, detail="The hphone number must be entered as a number")

    # بررسی صحت دانشکده
    def check_department(db: Session, department: str):
        valid_dp = {
            "فنی و مهندسی",
            "علوم پایه",
            "علوم انسانی",
            "دامپزشکی",
            "اقتصاد",
            "کشاورزی",
            "منابع طبیعی"
        }

        if department not in valid_dp:
            raise HTTPException(status_code=400, detail="The department is invalid")

    # بررسی صحت رشته تحصیلی
    def check_major(db: Session, major: str):
        valid_majors = ["مهندسی کامپیوتر", "مهندسی برق(الکترونیک)", "مهندسی برق(قدرت)", "مهندسی مکانیک و پلیمر",
                        "مهندسی معدن", "مهندسی عمران", "مهندسی شهرسازی"]
        if major not in valid_majors:
            raise HTTPException(status_code=400, detail="The major is invalid")

    # بررسی وضعیت تاهل
    def check_married(db: Session, married: str):
        if not (married == "مجرد" or married == "متاهل"):
            raise HTTPException(status_code=400, detail="Invalid marital status.")

    # بررسی صحت کد ملی
    def check_id(db: Session, id: int):
        student = db.query(models.Student).filter(models.Student.id == id).first()
        if student is not None:
            raise HTTPException(status_code=400, detail="This ID already exists")

        id_str = str(id)
        if len(id_str) != 10 or not id_str.isdigit():
            raise HTTPException(status_code=400, detail="The entered ID should be 10 digits")

        check = int(id_str[9])
        sum = 0
        for i in range(9):
            sum += int(id_str[i]) * (10 - i)
        c = sum % 11

        if not (c < 2 and check == c or c >= 2 and check == 11 - c):
            raise HTTPException(status_code=400, detail="Invalid ID number")



# PROFESSOR
class professor_datavalidation:

    # بررسی وجود استاد با استفاده از کد استاد
    def professor_exists_check(db: Session, lid: str):
        professor_lid = db.query(models.Professor).filter(models.Professor.lid == lid).first()
        if professor_lid is not None:
            raise HTTPException(status_code=409, detail="professor with this lid already exists")

    # بررسی صحت کد استاد
    def check_lid(db: Session, lid: str):
        if len(lid) != 6:
            raise HTTPException(status_code=400, detail="lid must be 6 characters")
        if not lid.isdigit():
            raise HTTPException(status_code=400, detail="lid must be number")

    # بررسی صحت نام و نام خانوادگی استاد
    def check_flname(db: Session, fname: str, lname: str):
        if len(fname) > 11 or len(lname) > 11:
            raise HTTPException(status_code=400, detail="The number of names cannot be more than 10")

        if not all('آ' <= char <= 'ی' or char == ' ' for char in (fname + lname)):
            raise HTTPException(status_code=400,
                                detail="The entered name should only contain Persian letters and should not contain numbers, special characters")

    # بررسی صحت کد ملی استاد
    def check_id(db: Session, id: int):
        professor = db.query(models.Professor).filter(models.Professor.id == id).first()
        if professor is not None:
            raise HTTPException(status_code=400, detail="This ID already exists")

        id_str = str(id)
        if len(id_str) != 10 or not id_str.isdigit():
            raise HTTPException(status_code=400, detail="The entered ID should be 10 digits")

        check = int(id_str[9])
        sum = 0
        for i in range(9):
            sum += int(id_str[i]) * (10 - i)
        c = sum % 11

        if not (c < 2 and check == c or c >= 2 and check == 11 - c):
            raise HTTPException(status_code=400, detail="Invalid ID number")

    # بررسی صحت دانشکده
    def check_department(db: Session, department: str):
        valid_dp = {
            "فنی و مهندسی",
            "علوم پایه",
            "علوم انسانی",
            "دامپزشکی",
            "اقتصاد",
            "کشاورزی",
            "منابع طبیعی"
        }

        if department not in valid_dp:
            raise HTTPException(status_code=400, detail="The department is invalid")

    # بررسی صحت رشته تحصیلی
    def check_major(db: Session, major: str):
        valid_majors = ["مهندسی کامپیوتر", "مهندسی برق(الکترونیک)", "مهندسی برق(قدرت)", "مهندسی مکانیک و پلیمر",
                        "مهندسی معدن", "مهندسی عمران", "مهندسی شهرسازی"]
        if major not in valid_majors:
            raise HTTPException(status_code=400, detail="The major is invalid")

    # بررسی صحت تاریخ تولد استاد
    def check_birth(db: Session, birth: str):
        if len(birth) != 10:
            raise HTTPException(status_code=400, detail="The entered date must be exactly 10 digits"
                                                        " and separated by periods")

        parts = birth.split('.')
        if len(parts) != 3:
            raise HTTPException(status_code=400, detail="The date must have three parts"
                                                        " (year, month and day) respectively.")

        year, month, day = parts
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            raise HTTPException(status_code=400, detail="The date entered must contain numbers")

        year = int(year)
        month = int(month)
        day = int(day)

        if not (1300 <= year <= 1402):
            raise HTTPException(status_code=400, detail="The entered year must be between 1300 and 1402")

        if not (1 <= month <= 12):
            raise HTTPException(status_code=400, detail="The month entered must be between 1 and 12")

        if (1 <= month <= 6) and not (1 <= day <= 31):
            raise HTTPException(status_code=400, detail="The day entered must be between 1 and 31")

        if (7 <= month <= 12) and not (1 <= day <= 30):
            raise HTTPException(status_code=400, detail="The day entered must be between 1 and 30")

    # بررسی صحت شهر محل تولد مرکز استان استاد
    def born_city(db: Session, born_city: str):
        markaz = ["اراک", "خرم آباد", "تهران", "اردبیل", "تبریز", "اصفهان", "اهواز", "ایلام", "بجنورد", "بیرجند", "مشهد",
                  "بندرعباس", "بوشهر", "ارومیه", "رشت", "زاهدان", "زنجان", "سمنان", "سنندج", "شیراز", "شهرکرد", "قزوین",
                  "قم", "کرج", "کرمان", "کرمانشاه", "گرگان", "همدان", "یاسوج", "یزد"]
        if not (born_city in markaz):
            raise HTTPException(status_code=400, detail="The entered province is not in the list of Iranian provinces"
                                                        " or the input was entered incorrectly")

    # بررسی صحت آدرس استاد
    def check_address(db: Session, address: str):
        if len(address) > 100:
            raise HTTPException(status_code=400, detail="The length of the address exceeds the limit (100 characters).")

    # بررسی صحت کد پستی استاد
    def check_postalcode(db: Session, postalcode: int):
        strpostalcode = str(postalcode)
        if len(strpostalcode) != 10 or not strpostalcode.isdigit():
            raise HTTPException(status_code=400, detail="postalcode must be 10 digits")

    # بررسی صحت شماره تماس همراه استاد
    def check_cphone(db: Session, cphone: str):
        if len(cphone) != 14 or not cphone[5:].isdigit():
            raise HTTPException(status_code=400, detail="The cphone number entered is not valid")
        if cphone[0:4] != "+98-":
            raise HTTPException(status_code=400, detail="The cphone number must start with +98")

    # بررسی صحت شماره تماس ثابت استاد
    def check_hphone(db: Session, hphone: str):
        if hphone.count('_') != 1:
            raise HTTPException(status_code=400, detail="The entered phone number must have two parts prefix"
                                                        " and fixed number and separated by _")

        parts = hphone.split('_')
        first = parts[0]
        second = parts[1]

        if len(first) != 3 or len(second) != 8:
            raise HTTPException(status_code=400, detail="The prefix must be three digits and"
                                                        " the landline number must be eight digits")

        if not (first.isdigit() and second.isdigit()):
            raise HTTPException(status_code=400, detail="The phone number must be entered as a number")



#COURSE
class course_datavalidation:

    # بررسی وجود درس با کد درس مشابه در دیتابیس
    def course_exists_check(db: Session, cid: str):
        course_cid = db.query(models.Course).filter(models.Course.cid == cid).first()
        if course_cid is not None:
            raise HTTPException(status_code=409, detail="Course with this cid already exists")

    # بررسی طول و نوع داده کد درس
    def check_cid(db: Session, cid: str):
        if len(cid) != 5:
            raise HTTPException(status_code=400, detail="cid must be 5 characters")
        if not cid.isdigit():
            raise HTTPException(status_code=400, detail="cid must be number")

    # بررسی صحت نام درس
    def check_cname(db: Session, cname: str):
        # بررسی طول نام دوره
        if len(cname) > 25:
            raise HTTPException(status_code=400, detail="The number of characters cannot be more than 25")

        # بررسی اعتبار حروف فارسی و فاصله در نام دوره
        for char in cname:
            if not ('آ' <= char <= 'ی' or char == ' '):
                raise HTTPException(status_code=400,
                                    detail="The entered name should only contain Persian letters and spaces")

    # بررسی صحت دانشکده
    def check_department_course(db: Session, department: str):
        # بررسی مقایسه دوره با دپارتمان های معتبر
        valid_dp = {
            "فنی و مهندسی",
            "علوم پایه",
            "علوم انسانی",
            "دامپزشکی",
            "اقتصاد",
            "کشاورزی",
            "منابع طبیعی"
        }

        if department not in valid_dp:
            raise HTTPException(status_code=400, detail="The department is invalid")

    # بررسی صحت تعداد واحد درسdatavalidation.py
    def check_credit(db: Session, credit: int):
        if not (1 <= credit <= 4):
            raise HTTPException(status_code=400, detail="Credit must be an integer between 1 and 4")


