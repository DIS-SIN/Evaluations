FROM python:3.6.8-stretch

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home appuser

ARG APP_SECRET_KEY
ARG APP_SQLALCHEMY_DATABASE_URI:
ARG APP_SENTRY_URL
ARG GOOGLE_APPLICATION_CREDENTIALS

WORKDIR /home/appuser


COPY app.py .
COPY departments_serializer.py .
COPY src src
RUN chown -R appuser:appuser .
USER appuser

CMD [ "flask", "run" ]


