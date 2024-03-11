FROM python:3.12


RUN groupadd -g 1001 -r web && useradd -r -u 1001 -g web -s /bin/bash -m -d /home/web web

RUN apt-get update -y

COPY --chown=web:web requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY --chown=web:web gunicorn-cfg.py /home/web/gunicorn-cfg.py
COPY --chown=web:web src/ /home/web/
WORKDIR /home/web

CMD gunicorn -c gunicorn-cfg.py server:app
