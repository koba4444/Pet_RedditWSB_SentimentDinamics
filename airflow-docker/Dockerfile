FROM ubuntu:latest
#WORKDIR /app

RUN apt-get update
RUN apt-get install -y python3 python3-pip



COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt


ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone



RUN apt-get update
RUN apt-get -y install git-all
RUN apt-get update
RUN apt-get -y install iputils-ping





EXPOSE 8080
RUN airflow db init
RUN airflow users create -u admin -f Peter -l Parker -r Admin -e spiderman@superhero.org -p admin
CMD airflow standalone
