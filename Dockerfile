FROM python:3.7-slim-buster

WORKDIR /relevanC
COPY . .

RUN pip3 install pipenv
RUN pipenv install -d

ENTRYPOINT ["pipenv", "run", "doit"]
CMD ["run_script"]

