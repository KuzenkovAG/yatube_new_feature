# Yatube v.1.0.0 New Features
Social network. 

### Deployed on server
[PythonAnyWhere] <- current working version 

## Features
- Signup and login.
- Create Post.
- Create Comment for Post.
- View Posts and comments of other Users.
- Become follower of other user.

### New features
- Users have personal cabinet where can change email, name, photo.
- Post have counter of views.
- Post have likes.
- New design of pages.

## History of Yatube project
- v.1.0.0 [New Features] <- You are here
- v.0.4.0 [Final]  - Add ability to follow users. Add comments to posts.
- v.0.3.0 [UnitTest] - Create tests.
- v.0.2.0 [Forms] - Add ability to create new posts. Add auth of User.
- v.0.1.0 [Community] - Ability to view posts.

## Tech
- Python 3.9
- Django 2.2

#### Tested Python version
Python 3.7-3.9


## Installation (for Windows)
Clone repository
```sh
git clone git@github.com:KuzenkovAG/yatube_new_feature.git
```
Install environment
```sh
cd yatube_new_feature/
```
```sh
py -3.9 -m venv venv
```
Activate environment
```sh
source venv/Scripts/activate
```
Install requirements
```sh
pip install -r requirements.txt
```
Create .env
```sh
touch yatube/yatube/.env
```
Open .env and save secret key
```sh
nano yatube/yatube/.env
DJANGO_SECRET_KEY = 'as!b)khi$*#wm!!&@=+^vzve^u&9o%0fsxn7fkfu$1x-)2on^h'
```
Make migrate
```sh
python yatube/manage.py migrate
```
Run server
```sh
python yatube/manage.py runserver
```

## Usage
Index page
```sh
http://127.0.0.1:8000/
```
Page of post
```sh
http://127.0.0.1:8000/posts/1/
```
Create post
```sh
http://127.0.0.1:8000/create/
```
Page of User
```sh
http://127.0.0.1:8000/profile/user_name/
```
Page of group
```sh
http://127.0.0.1:8000/group/group_slug/
```
Page of follows
```sh
http://127.0.0.1:8000/follow/
```
Page of personal account of User
```sh
http://127.0.0.1:8000/account/
```


## Author
[Alexey Kuzenkov]

   [PythonAnyWhere]: <https://alexey241390.pythonanywhere.com/>

   [Alexey Kuzenkov]: <https://github.com/KuzenkovAG>
   [New Features]: <https://github.com/KuzenkovAG/yatube_new_feature>
   [Final]: <https://github.com/KuzenkovAG/yatube_final>
   [UnitTest]: <https://github.com/KuzenkovAG/yatube_tests>
   [Forms]: <https://github.com/KuzenkovAG/yatube_forms>
   [Community]: <https://github.com/KuzenkovAG/yatube_community>
