FROM python:3.11-slim

WORKDIR /app

RUN python3 -m venv .venv
RUN pip install pip --upgrade

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app/ .

CMD [ "streamlit", "run", "ui.py", "--server.address=0.0.0.0" ]
