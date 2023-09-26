FROM python:3.11-slim

WORKDIR /app

RUN python3 -m venv .venv
RUN pip install --no-cache-dir --upgrade pip
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN apt-get update && apt-get install -y curl && apt-get autoremove -y

COPY app/app .

CMD [ "streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0" ]
