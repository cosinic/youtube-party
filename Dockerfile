FROM python:3.7.4-alpine
EXPOSE 5000 
WORKDIR /app
ENV FLASK_APP=__init__.py

COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY src /app
CMD flask run --host=0.0.0.0