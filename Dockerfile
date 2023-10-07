FROM python:3.7

RUN mkdir /secret_marks

WORKDIR /secret_marks

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
