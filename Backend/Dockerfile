FROM python:3.7.3


ENV http_proxy http://wwwproxy.unimelb.edu.au:8000

ENV https_proxy http://wwwproxy.unimelb.edu.au:8000

ENV PYTHONUNBUFFERED 1



RUN mkdir /backend

WORKDIR /backend

ADD . /backend

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "python","app.py" ]