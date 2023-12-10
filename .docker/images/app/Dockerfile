FROM python:3.11-slim

# Label for github packages
LABEL org.opencontainers.image.source=https://github.com/lelouvincx/Chinh-Dinh-training
LABEL org.opencontainers.image.description="Data generator (called upstream-app), generates data to source_db."

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

COPY app .

CMD [ "streamlit", "run", "app/streamlit_app.py", "--server.address=0.0.0.0" ]
