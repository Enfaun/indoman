FROM alpine AS build-env

COPY ./requirements.txt /app/
WORKDIR /app

RUN apk add --no-cache python3
RUN apk add --no-cache --virtual deps build-base python3-dev

RUN python3 -m ensurepip --upgrade
RUN pip3 install --no-cache-dir --ignore-installed -r ./requirements.txt

COPY . /app

RUN apk del deps apk-tools busybox
RUN yes | pip3 uninstall --no-cache-dir setuptools pip
RUN rm -r /tmp/*
RUN rm -r /lib/apk
RUN rm /bin/busybox

FROM scratch

COPY --from=build-env / /
WORKDIR /app

EXPOSE 4636
ENV PYTHONUNBUFFERED=1

CMD ["python3", "-m", "indoman"]

