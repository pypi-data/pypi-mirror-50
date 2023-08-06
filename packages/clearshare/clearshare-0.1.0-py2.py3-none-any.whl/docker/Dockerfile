FROM python:3.7-alpine
COPY deploy /app
COPY specs /app/docker/specs
COPY deploy/ipfs.yml /app/specs/ipfs.yml
COPY hosts /etc/hosts
ENV CLEARSHARE_HOME=/app
WORKDIR /app
RUN pip install --upgrade pip && \
    pip install --upgrade -r requirements.txt && \
    nslookup clearshare.local && \
    mkdir /app/home
EXPOSE 8095
HEALTHCHECK CMD curl --fail http://clearshare.local:8095/ || exit 1
CMD ["clearshare_app.py"]
