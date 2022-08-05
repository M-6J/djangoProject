## Project version3
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
- Team :
- Member : 团队里 有3种人， member，manager，creater（super manager）
