FROM python:3.9-slim
EXPOSE 5555

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
WORKDIR /app

USER nobody
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "nginx-ldap-connector:app" ]
