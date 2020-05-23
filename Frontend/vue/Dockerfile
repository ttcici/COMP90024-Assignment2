FROM node:latest


ENV http_proxy http://wwwproxy.unimelb.edu.au:8000
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000


RUN mkdir /front-end
WORKDIR /front-end
ADD . /front-end

RUN npm install
RUN npm run build

EXPOSE 8080

CMD [ "npm","run" ,"server" ]