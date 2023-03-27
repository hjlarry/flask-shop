### Build and install packages
FROM python:3.10

# Install Python dependencies
WORKDIR /app
COPY requirements.txt requirements.txt
COPY plugin_example  plugin_example
COPY flaskshop  flaskshop
COPY app.py  app.py

RUN pip install --no-cache -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]
