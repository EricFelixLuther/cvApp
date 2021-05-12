FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY cv_App/ /code/
RUN mkdir /var/log/cvapp
RUN pip install -r requirements.txt
RUN apt -y update && apt -y upgrade && autoremove && autoclean
RUN apt -y install wkhtmltopdf

COPY entrypoint.sh /entrypoint.sh
RUN ["chmod", "+x", "/entrypoint.sh"]
ENTRYPOINT ["/entrypoint.sh"]


