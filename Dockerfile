FROM python:3.10.6-slim-buster
COPY . /cache-app
WORKDIR /cache-app
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "cache_app.py" ]