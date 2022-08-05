## Project version3
- 主要任务是 前端和后端 链接 Refactoring
- Django Backend Final Version

- python -m pip install --upgrade pip
- Python 3.10.2
- Django 4.0.6



### use venv virtual environment
- python -m venv venv
- venv/scripts/activate

### 步骤
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser : make admin account
- python manage.py runserver

### model介绍
- Profile : 用户 model
- Notice ： 邀请技能
- Task : 任务，用户可以做Task
- Team : 团队有6种，可以选择段对种类
- Member : 团队里有3种人， member，manager，creator（super manager）

### view介绍

#### ProfileApp
- notice_view : 招待技能， 用户可以看见自己是否被招待
