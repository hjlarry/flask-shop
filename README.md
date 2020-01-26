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

**First, Create a virtual environment**
```
pip3 install virtualenv
mkdir ~/.virtualenvs/flask-shop/ && cd ~/.virtualenvs/flask-shop/
virtualenv --no-site-packages .
```

**Second, Clone and Install dependence**
```
git clone https://github.com/hjlarry/flaskshop
cd flask-shop
# I use autoenv instead of manual change to virtual env
source ~/.virtualenvs/flask-shop/bin/activate
pip3 install -r requirements.txt
```

**Third, Init db and run**
```
# modify flaskshop/setting.py
export FLASK_APP=autoapp.py
export FLASK_DEBUG=1
flask db init
flask db migrate
flask db upgrade
flask seed
flask run
```

If the js files has been modified, you need to:
```
npm install
npm run build
```