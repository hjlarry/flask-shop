# flask shop


## Introduction
This project is a front page copy of [saleor](https://github.com/mirumee/saleor), but write with flask. 
It havn`t complete yet.

## ScreenShot
![ScreenShot](ScreenShot/1.png)
![ScreenShot](ScreenShot/2.png)
![ScreenShot](ScreenShot/3.png)
![ScreenShot](ScreenShot/4.png)



## Quickstart

```
git clone https://github.com/hjlarry/flaskshop
cd flask-shop
# please create virual env
pip3 install -r requirements.txt
npm install
export FLASK_APP=autoapp.py
export FLASK_DEBUG=1
flask db init
flask db migrate
flask db upgrade
python flaskshop/random_data.py
npm start
```