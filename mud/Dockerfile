FROM python:3.8
WORKDIR /home/mud
RUN pip install requests
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /home/mud
ENTRYPOINT ["/home/mud/mud.py"]
