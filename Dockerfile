FROM python:3.9-slim 

WORKDIR /
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]