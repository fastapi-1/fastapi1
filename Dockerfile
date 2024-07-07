FROM python:3.12.3

WORKDIR /var/www

COPY /sql_app/requirements.txt .

RUN pip install -r requirements.txt

COPY sql_app .

CMD ["fastapi", "run", "main.py"]
