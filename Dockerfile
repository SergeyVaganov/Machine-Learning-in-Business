FROM python:3.9
LABEL maintainer="sp.vaganov@yandex.ru"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8180
EXPOSE 8181
VOLUME /app/app/models
COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]