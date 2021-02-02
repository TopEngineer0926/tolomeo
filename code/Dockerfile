FROM python:3.7-alpine
ADD . ./code
WORKDIR /code
ENV FLASK_APP=app/app.py
#ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers && apk add bash
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install pytest
RUN pip3 install requests
EXPOSE 5000
CMD ["flask", "run"]