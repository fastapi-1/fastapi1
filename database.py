# ایمپورت توابع مورد نیاز از SQLAlchemy
from sqlalchemy import create_engine  # برای ایجاد موتور اتصال به دیتابیس
from sqlalchemy.ext.declarative import declarative_base  # برای تعریف پایه برای مدل‌های دیتابیس
from sqlalchemy.orm import sessionmaker  # برای ایجاد کننده نشست برای ارتباط با دیتابیس


# آدرس دیتابیس SQLite یا PostgreSQL
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# ایجاد موتور اتصال به دیتابیس
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # ارتباط در حالت تک نخ (برای SQLite)
)

# تولید کننده نشست برای ارتباط با دیتابیس
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# تعریف پایه برای ایجاد مدل‌های دیتابیس
Base = declarative_base()

# SessionLocal برای ایجاد نشست های جدید برای ارتباط با دیتابیس استفاده می‌شود.
# autocommit=False به معنی غیرفعال بودن خودکار commit تراکنش هااست، که بهینه سازی عملیات دیتابیس را فراهم می‌کند.
# autoflush=False به معنی غیرفعال بودن خودکار flush تراکنش هااست، که کنترل دقیق‌تری روی زمان ارسال داده ها به دیتابیس فراهم میکند.
# bind=engine به معنی متصل کردن نشست‌های جدید به موتور دیتابیسی است که ارتباط را برقرار می‌کند.

# Base یک کلاس پایه است که توسط declarative_base() ایجاد شده است و مدل‌های دیتابیسی را تعریف و ایجاد می‌کند.
# این کلاس برای تعریف جداول دیتابیس و نگهداری ساختارهای مرتبط با دیتابیس به کار می‌رود


