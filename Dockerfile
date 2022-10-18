FROM python:latest

WORKDIR /

EXPOSE 8080/tcp

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

RUN python -m unittest -f tests/test.py

CMD ["python3", "main.py", "--file=binlist-data.csv"]
