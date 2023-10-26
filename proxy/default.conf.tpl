server {
  listen ${LISTEN_PORT};

  location /coordinates/ {
    proxy_pass http://coordinates_api:9000/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade "$http_upgrade";
    proxy_set_header Connection "upgrade";
    proxy_set_header X-Real-IP "$remote_addr";
    proxy_set_header X-Forwarded-For "$proxy_add_x_forwarded_for";
    proxy_set_header X-Forwarded-Proto "$scheme";
    proxy_buffers 16 32k;
    proxy_buffer_size 64k;
    proxy_connect_timeout       600;
    proxy_send_timeout          600;
    proxy_read_timeout          600;
    send_timeout                600;
  }
}
