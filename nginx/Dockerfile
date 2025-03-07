FROM nginx:latest

RUN mkdir -p /etc/nginx/ssl

# Копируем конфиг
COPY nginx.conf /etc/nginx/nginx.conf

# Копируем сертификаты
COPY certs/fullchain.pem /etc/nginx/ssl/
COPY certs/privkey.pem /etc/nginx/ssl/

# Установка прав доступа к сертификатам
RUN chmod 600 /etc/nginx/ssl/*

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
