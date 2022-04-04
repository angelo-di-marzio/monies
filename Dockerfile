FROM python:3.9
WORKDIR /app

# copy requirements and install before copying code to use Docker cache for dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app .


