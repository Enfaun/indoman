FROM python:alpine AS build-env

RUN apk add --no-cache --virtual deps build-base python3-dev

COPY ./requirements.txt /app/
WORKDIR /app

RUN pip3 install --no-cache-dir -r ./requirements.txt

COPY . /app

RUN apk del deps apk-tools
RUN rm -r /tmp/*

FROM scratch

COPY --from=build-env / /
WORKDIR /app

EXPOSE 4636

CMD ["python3", "-m", "indoman"]
