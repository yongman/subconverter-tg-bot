FROM ubuntu:20.04

RUN apt update && apt install -y python3 python3-pip curl && rm -rf /var/lib/apt/lists/* && pip install python-telegram-bot

COPY clash_rules.py /
COPY call_http.sh /

RUN chmod +x clash_rules.py && chmod +x call_http.sh

ENTRYPOINT ["python3", "/clash_rules.py"]
