# fanxiangce
An album website made by Flask and Python (翻相册). 

## ScreenShots
User page:  
![user page](https://raw.githubusercontent.com/greyli/fanxiangce/master/screenshots/user.png)

Album page:  
![album page](https://raw.githubusercontent.com/greyli/fanxiangce/master/screenshots/album.png)

Edit page:  
![edit page](https://raw.githubusercontent.com/greyli/fanxiangce/master/screenshots/edit.png)

Photo page:  
![photo page](https://raw.githubusercontent.com/greyli/fanxiangce/master/screenshots/photo.png)

## Extensions and Plugins

- Flask==0.11.1
- Flask-Bootstrap==3.0.3.1
- Flask-Login==0.3.1
- Flask-Mail==0.9.0
- Flask-Migrate==1.1.0
- Flask-Moment==0.2.1
- Flask-Script==0.6.6
- Flask-SQLAlchemy==1.0
- Flask-Uploads==0.2.1
- Flask-WTF==0.12
- Isotope
- Lightbox2
- jQuery-UI

## Installation

Clone it from Github:

```
$ git clone https://github.com/greyli/fanxiangce.git
```
Use `virtualenv` to create a virtual enviroment and activate it (Optional but Recommend).  
Then install packages:
```
$ pip install -r requirements/prod.txt
```
Create database and migration file:
```
$ cd fanxiangce
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```
Run it by Flask-Script's command `runserver`:
```
$ python manage.py runserver
```
Now Go to http://127.0.0.1:5000/

## Sub-Project
https://github.com/greyli/image-wall

## More details
- fanxiangce is 翻相册's pinyin (翻: flip, 相册: album).
- [fanxiangce.com](http://fanxiangce.com) now is only an old demo page.
- More information can be found on ['Hello, Flask!'](https://zhuanlan.zhihu.com/flask) -- an column about Flask and Web development.

## License
This demo application is licensed under the MIT license: http://opensource.org/licenses/mit-license.php
