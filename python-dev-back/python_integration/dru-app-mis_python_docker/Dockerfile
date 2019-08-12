FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

EXPOSE 8049 
ENTRYPOINT ["sh", "-c","/app/start.sh" ]
