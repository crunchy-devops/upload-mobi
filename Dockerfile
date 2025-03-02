FROM ubuntu

RUN apt-get update
RUN apt-get -y install python3 python3-pip vim iputils-ping

ADD templates/. /opt/templates
#ADD uploads   /opt/uploads
COPY requirements.txt .
RUN pip install -r requirements.txt --break-system-packages
WORKDIR /opt
COPY app.py /opt
ENV FLASK_APP=/opt/app.py
EXPOSE 80
ENTRYPOINT ["flask", "run", "--port=80", "--host=0.0.0.0"]