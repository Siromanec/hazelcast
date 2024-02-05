FROM python:3.10-alpine
WORKDIR /client
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY hazelcast-client.py .
CMD ["sh", "-c", "python3 hazelcast-client.py -c $MC_DEFAULT_CLUSTER"]


