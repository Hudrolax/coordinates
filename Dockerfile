FROM python:3.11.4-alpine3.18

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp_req/requirements.txt
COPY ./requirements.dev.txt /tmp_req/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app

WORKDIR /app
EXPOSE 9000
EXPOSE 5900

ENV PYTHONPATH=/app

ARG DEV=false

# install dependencies
RUN apk update && apk upgrade && \
    apk add --no-cache --virtual .build-deps \
    alpine-sdk \
    curl \
    wget \
    unzip \
    gnupg \
    gcc \
    linux-headers \
    python3-dev \
    musl-dev && \
  apk add --no-cache \
    xvfb \
    x11vnc \
    fluxbox \
    xterm \
    libffi-dev \
    openssl-dev \
    zlib-dev \
    bzip2-dev \
    readline-dev \
    sqlite-dev \
    git \
    nss \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    chromium \
    chromium-chromedriver

# config x11vnc
RUN mkdir ~/.vnc
ARG VNC_PASS
RUN x11vnc -storepasswd ${VNC_PASS} ~/.vnc/passwd

RUN python -m venv /py && \
  /py/bin/pip install --upgrade pip && \
  /py/bin/pip install --no-cache-dir -r /tmp_req/requirements.txt && \
  if [ $DEV = "true" ]; \
  then /py/bin/pip install -r /tmp_req/requirements.dev.txt ; \
  fi && \
  apk del .build-deps && \
  rm -rf /tmp_req && \
  chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"
ENV DISPLAY=:0

CMD ["run.sh"]