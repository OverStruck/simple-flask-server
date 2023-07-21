FROM python:3.8-slim-buster
# FROM python
# update pip
RUN python -m pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app.py .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=7878", "--with-threads", "--debug"]