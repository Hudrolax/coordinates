FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="hud.net.ru"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./run.sh /run.sh

USER root

RUN mkdir -p /vol/static/swapped && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]
