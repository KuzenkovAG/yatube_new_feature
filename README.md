# Yatube New Features
Social network. 

### Deploy on server
[Link] <- current working version 

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

## History
- [Now] <- You are here
- [Yatube final] Add ability to follow users
- [Yatube unittest] Create tests. Add comments for posts.
- [Yatube forms] Add ability to create new posts; Add registration of User.
- [Yatube comunity] Add ability to view post.

## Tech
- Python 3.9
- Django 2.2

## Requirements
Python 3.7-3.9


## Installation (for Windows)
1. Clone repository on your PC
```sh
git clone ...
```
2. Install vertual enviroment
```sh
py -3.9 -m venv venv
```
3. Install requirements
```sh
pip install -r requirements.txt
```
4. Make migrations and run server
```sh
python manage.py migrate
python manage.py runserver
```

## Usage
Index page
```sh
http://127.0.0.1:8000/
```

Page of post (if post with id=1 exists)
```sh
http://127.0.0.1:8000/posts/1/
```

Page of user_name (if user with username=user_name exists)
```sh
http://127.0.0.1:8000/profile/user_name/
```

Page of group (if group with slug=group_slug exists)
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

   [link]: <https://alexey241390.pythonanywhere.com/>

   [Alexey Kuzenkov]: <https://github.com/KuzenkovAG>
   [Now]: <https://github.com/KuzenkovAG/yatube_new_feature>
   [Yatube final]: <https://github.com/KuzenkovAG/yatube_final>
   [Yatube unittest]: <https://github.com/KuzenkovAG/yatube_tests>
   [Yatube forms]: <https://github.com/KuzenkovAG/yatube_forms>
   [Yatube comunity]: <https://github.com/KuzenkovAG/yatube_community>