FROM python:3.7.1

LABEL MAINTAINER="jianshi@cuhk.edu.hk"

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements-web.txt /requirements-web.txt

RUN pip install --upgrade pip && \
    pip install -r requirements-web.txt

WORKDIR /app

COPY ./src /app

EXPOSE 8050

CMD [ "python", "app.py" ]