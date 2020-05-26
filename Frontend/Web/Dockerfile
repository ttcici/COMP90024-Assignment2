# Team 16: COMP90024-Assignment2
## Team Members:
#Qingmeng Xu, 969413
#Tingqian Wang, 1043988
#Zhong Liao, 1056020
#Cheng Qian, 962539
#Zongcheng Du, 1096319


FROM node:latest


ENV http_proxy http://wwwproxy.unimelb.edu.au:8000
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000


RUN mkdir /front-end
WORKDIR /front-end
ADD . /front-end

RUN npm install
RUN npm install express

EXPOSE 8080

CMD [ "node","server.js" ]