FROM python:3.7.5-slim

WORKDIR /usr/src/app

COPY ph_daily.py requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python", "ph_daily.py"]