FROM public.ecr.aws/y5z1i2v3/zhongpengqun:python2.7

LABEL org.opencontainers.image.authors="zhongpengqun2022@gmail.com"

RUN mkdir -p /var/www
WORKDIR /var/www/
COPY daydayup/ /var/www/

RUN pip install --upgrade pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# Must set "--host", "0.0.0.0", otherwise will unable be accessed from external.
CMD ["python", "app.py", "runserver", "--host", "0.0.0.0"]

EXPOSE 5000

