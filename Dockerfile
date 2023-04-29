FROM python:2.7

MAINTAINER ZhongPengQun

RUN mkdir -p /var/www
WORKDIR /var/www/
COPY daydayup/ /var/www/

RUN pip install --upgrade pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD ["python", "app.py", "runserver"]

EXPOSE 5000

