FROM python:3.10.8
 
ENV PYTHONUNBUFFERED 1
WORKDIR /stripeapi
COPY . /stripeapi
COPY requirements.txt /stripeapi/requirements.txt
COPY stripeapi/wsgi.py /stripeapi/wsgi.py
COPY stripeapi/settings.py /stripeapi/settings.py

RUN pip install --no-cache-dir -r /stripeapi/requirements.txt

RUN pip install gunicorn

EXPOSE 8000
CMD ["gunicorn","--bind", ":8000", "stripeapi.wsgi:application"]