FROM python:3.11

WORKDIR /code

RUN apt update
RUN apt install -y cron
RUN apt install -y vim
COPY ml-work-cronjob /etc/cron.d/ml-work-cronjob
RUN crontab /etc/cron.d/ml-work-cronjob

COPY note/train_img /code/train_img/
COPY src/mnist/main.py /code/
COPY src/mnist/model/ /code/
COPY run.sh /code/run.sh

RUN chmod +x /code/run.sh

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade git+https://github.com/nicou11/mnist.git@0.4/model

CMD ["sh", "run.sh"]
