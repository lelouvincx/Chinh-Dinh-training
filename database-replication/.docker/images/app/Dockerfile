FROM python:3.11-slim

# Label for github packages
LABEL org.opencontainers.image.source https://github.com/lelouvincx/Chinh-Dinh-training

WORKDIR /app

# Activate python virtual environment
RUN python3 -m venv .venv
RUN . .venv/bin/activate

RUN pip install --no-cache-dir --upgrade pip

# Install requirements
COPY .docker/images/app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install curl
RUN apt-get update && apt-get install -y --no-install-recommends curl && apt-get autoremove -y

COPY app/app .

CMD [ "streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0" ]
