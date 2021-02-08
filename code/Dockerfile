FROM python:3.7-alpine
RUN apk add --no-cache gcc musl-dev linux-headers && apk add bash
WORKDIR /code
COPY ./ /code/
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP=app/app.py
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install psycopg2
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]