# 
# FROM python:3.11-slim as build
FROM python:3.11
# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./ /code

# 
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]