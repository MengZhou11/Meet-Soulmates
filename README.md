# 运行

运行环境


python3.8
pip install django==2.1.10

pip install -r requirements.txt

每次更新之后运行


python manage.py makemigrations

python manage.py migrate

运行服务器


python manage.py runserver

成功运行在本地时显示


System check identified no issues (0 silenced).
April 21, 2022 - 21:53:07
Django version 2.1.10, using settings 'MeetSoulmates.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

通过 http://127.0.0.1:8000/ 访问网站

# 修改

HTML注意事项


CSS和JS等放在MeetSoulmates/static的对应文件夹下

调用时使用/static/作为前缀目录

所有链接不能指向html文件，而是指向一个url，比如index而不是index.html

url所对应的前端在soul/urls.py 以及 soul/view/home.py 里更改

把网页连上去就行，随便复制一个已经写好的改一下名字就能加上，要加什么复杂的东西跟我说我来改。

访问网页具体流程为 url -> view -> html

不能从html直接访问其他html，所以提交表单的时候要指向url

差不多就这样，我也没试过，报错了发群里看看。

