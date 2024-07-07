FROM python:3.12.3

WORKDIR /var/www

COPY  /fastapi1/sql_app/requirments.txt .

RUN pip install -r requirments.txt

COPY sql_app .

CMD ["fastapi", "run", "main.py"]
