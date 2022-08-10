### Build and install packages
FROM python:3.8

# Install Python dependencies
COPY requirements.txt /app/
COPY plugin_example/ app/plugin_example/
WORKDIR /app
RUN pip install -i https://pypi.douban.com/simple -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["flask", "run"]
