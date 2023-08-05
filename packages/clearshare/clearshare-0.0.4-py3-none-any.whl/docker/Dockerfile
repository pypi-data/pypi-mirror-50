FROM python:3.7-alpine
COPY deploy /app
COPY specs /app/specs
COPY hosts /etc/hosts
WORKDIR /app
RUN pip install --upgrade pip && \
    pip install --upgrade -r requirements.txt && \
    nslookup clearshare.local
EXPOSE 8095
HEALTHCHECK CMD curl --fail http://clearshare.local:8095/ || exit 1
CMD ["app.py"]
