## Project version3
- 主要任务是 前端和后端 链接 Refactoring
- Django Backend Final Version

- python -m pip install --upgrade pip
- Python 3.10.2
- Django 4.0.6
- pip install django-cors-headers

## 注意事项
- csrf 处理
- cors 处理


### use venv virtual environment
- python -m venv venv
- venv/scripts/activate

### 步骤
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser : make admin account
- python manage.py runserver

## model介绍
#### profileAPP
- Profile : 用户 model
- Notice ： 邀请技能

#### projectAPP
- Project : 项目

#### taskAPP
- Task : 任务，用户可以做Task

#### teamAPP
- Team : 团队有6种，可以选择段对种类
- Member : 团队里有3种人， member，manager，creator（super manager）

## view介绍

#### ProfileApp
- notice_view : 邀请技能， 用户可以看见邀请
- accept ： 接受邀请， 用户可以选择是否被邀请
- signup ： 用户注册，（email，username，passowrd）
- login ： 用户登录 ，（username，password）
- detail :
- edit :
- add_friend : 加朋友技能

#### ProjectAPP
- manage ： 确认用户 team_id 然后 返还 team 项目
- create ： 创建项目
- detail ： 看项目详细内容
- update ： 修改项目
- delete :  删除项目

#### TaskAPP


#### TeamAPP
- team_managing ：管理团队
- team_create : 团队创建
- team_detail : 查看团队信息
- verify : 认证
- invite_member : 发邀请
- del_member : 删除 团队成员
- promote : 升级 团队成员 -> 团队管理者
- degrade : 降低 团队管理者 -> 团队成员
