FROM python:3.7-alpine
RUN apk add --no-cache gcc musl-dev linux-headers bash postgresql-dev python3-dev
WORKDIR /code
COPY ./ /code/
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt