FROM python:3.11-slim

COPY r_prod.txt /app/

WORKDIR /app

RUN pip install -r r_prod.txt

COPY app /app/app

COPY run.py /app/

EXPOSE 8080

CMD ["python", "run.py"]
