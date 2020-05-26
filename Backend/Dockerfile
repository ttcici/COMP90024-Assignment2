#Team 16: COMP90024-Assignment2
#Team Members:
#Qingmeng Xu, 969413
#Tingqian Wang, 1043988
#Zhong Liao, 1056020
#Cheng Qian, 962539
#Zongcheng Du, 1096319

FROM python:3.7.3


ENV http_proxy http://wwwproxy.unimelb.edu.au:8000

ENV https_proxy http://wwwproxy.unimelb.edu.au:8000

ENV PYTHONUNBUFFERED 1



RUN mkdir /back-end

WORKDIR /back-end

ADD . /back-end

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "nohup", "python3","app.py" ,"&" ]